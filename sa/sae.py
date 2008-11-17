##
## Service Activation Engine
##
from noc.sa.models import Activator
from noc.cm.models import Config

from noc.sa.sae_stream import RPCStream,file_hash
import asyncore,socket,logging,time,threading,datetime,traceback,os
from noc.sa.protocols.sae_pb2 import *
from noc.sa.models import TaskSchedule
from noc.lib.fileutils import read_file

##
## Manifest for activator
##
ACTIVATOR_MANIFEST=[
    "__init__.py",
    "sa/__init__.py",
    "sa/activator.py",
    "sa/sae_stream.py",
    "sa/trapcollector.py",
    "sa/protocols/__init__.py",
    "sa/protocols/sae_pb2.py",
    "sa/actions/",
    "sa/profiles/",
    "lib/__init__.py",
    "lib/ip.py",
    "lib/registry.py",
    "lib/daemon.py",
    "lib/fileutils.py",
    "lib/ecma48.py",
    "scripts/noc-activator.py",
]

##
##
##
class Service(SAEService):
    def get_controller_activator(self,controller):
        return Activator.objects.get(name=self.sae.streams.get_name(controller.stream))
    ##
    ## RPC interfaces
    ##
    def ping(self,controller,request,done):
        done(controller,response=PingResponse())
        
    def register(self,controller,request,done):
        try:
            activator=Activator.objects.get(name=request.name)
        except Activator.DoesNotExist:
            logging.error("Unknown activator '%s'"%request.name)
            e=Error()
            e.code=ERR_UNKNOWN_ACTIVATOR
            e.text="Unknown activator '%s'"%request.name
            done(controller,error=e)
            return
        logging.info("Registering activator '%s'"%request.name)
        self.sae.register_activator(request.name,controller.stream)
        r=RegisterResponse()
        done(controller,response=r)
        
    def manifest(self,controller,request,done):
        done(controller,response=self.sae.activator_manifest)
        
    def software_upgrade(self,controller,request,done):
        r=SoftwareUpgradeResponse()
        for n in request.names:
            u=r.codes.add()
            u.name=n
            u.code=read_file(n)
        done(controller,response=r)
        
    def get_trap_filter(self,controller,request,done):
        activator=self.get_controller_activator(controller)
        r=TrapFilterResponse()
        for c in Config.objects.filter(activator=activator,trap_source_ip__isnull=False):
            profile=c.profile
            if profile.oid_trap_config_changed is None:
                continue
            f=r.filters.add()
            f.ip=c.trap_source_ip
            a=f.actions.add()
            a.oid=profile.oid_trap_config_changed
            a.actions.append(TA_NOTIFY_CONFIG_CHANGE)
        done(controller,response=r)
    
    def notify_trap_config_change(self,controller,request,done):
        activator=self.get_controller_activator(controller)
        try:
            c=Config.objects.get(activator=activator,trap_source_ip=request.ip)
        except Config.DoesNotExist:
            e=Error()
            e.code=ERR_UNKNOWN_TRAP_SOURCE
            e.text="Unknown trap source '%s'"%request.ip
            done(controller,error=e)
            return
        logging.info("%s configuration changed (Notified by trap)"%(c.repo_path))
        c.next_pull=min(c.next_pull,datetime.datetime.now()+datetime.timedelta(minutes=10))
        c.save()
        done(controller,NotifyResponse())
##
##
##
class SAEStream(RPCStream):
    def __init__(self,service,sock):
        RPCStream.__init__(self,service)
        logging.debug("Attaching SAEStream to socket")
        self.set_socket(sock)
        
    def handle_close(self):
        RPCStream.handle_close(self)
        self.service.sae.on_stream_close(self)

##
## Asyncronous listener socket
##
class Listener(asyncore.dispatcher):
    def __init__(self,sae,address,port):
        asyncore.dispatcher.__init__(self)
        self.sae=sae
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((address,port))
        self.listen(5)
    
    def handle_accept(self):
        self.sae.on_new_connect()
##
##
##
class StreamFactory(object):
    def __init__(self,sae):
        self.sae=sae
        self.name_by_stream={} # stream->name
        self.stream_by_name={} # name->stream
        
    def register(self,stream,name=None):
        logging.debug("register(%s,%s)"%(str(stream),name))
        self.name_by_stream[stream]=name
        if name:
            self.stream_by_name[name]=stream
    
    def unregister(self,stream):
        logging.debug("unregister(%s)"%str(stream))
        name=self.name_by_stream[stream]
        del self.name_by_stream[stream]
        if name:
            del self.stream_by_name[name]
    
    def get_name(self,stream):
        return self.name_by_stream[stream]
        
    def get_stream(self,name):
        return self.stream_by_name[name]
##
## SAE Supervisor
##
class SAE(object):
    def __init__(self,address,port):
        self.address=address
        self.port=port
        self.service=Service()
        self.service.sae=self
        self.streams=StreamFactory(self)
        # Periodic tasks
        self.active_periodic_tasks={}
        self.periodic_task_lock=threading.Lock()
        #
        self.activator_manifest=None
    
    def build_manifest(self):
        logging.debug("Building manifest")
        self.activator_manifest=ManifestResponse()
        for f in ACTIVATOR_MANIFEST:
            if f.endswith("/"):
                for dirpath,dirnames,filenames in os.walk(f):
                    for f in [f for f in filenames if f.endswith(".py")]:
                        path=os.path.join(dirpath,f)
                        cs=self.activator_manifest.files.add()
                        cs.name=path
                        cs.hash=file_hash(path)
            else:
                cs=self.activator_manifest.files.add()
                cs.name=f
                cs.hash=file_hash(f)

    def run(self):
        self.build_manifest()
        logging.debug("Starting listener at %s:%d"%(self.address,self.port))
        self.listener=Listener(self,self.address,self.port)
        last_cleanup=time.time()
        last_task_check=time.time()
        while True:
            asyncore.loop(timeout=1,count=1)
            if time.time()-last_task_check>10:
                self.periodic_task_lock.acquire()
                tasks = TaskSchedule.get_pending_tasks(exclude=self.active_periodic_tasks.keys())
                self.periodic_task_lock.release()
                if tasks:
                    for t in tasks:
                        self.run_periodic_task(t)
    ##
    ## Periodic tasks
    ##
    def run_periodic_task(self,task):
        logging.debug(u"New task running: %s"%unicode(task))
        t=threading.Thread(name=task.periodic_name,target=self.periodic_wrapper,kwargs={"task":task})
        self.periodic_task_lock.acquire()
        self.active_periodic_tasks[task.id]=t
        self.periodic_task_lock.release()
        t.start()
    
    def periodic_wrapper(self,task):
        logging.info(u"Executing %s"%unicode(task))
        tb=None
        try:
            status=task.periodic_class(self).execute()
        except:
            tb=traceback.format_exc()
            status=False
        logging.info(u"Task %s is terminated with '%s'"%(unicode(task),status))
        if status:
            timeout=task.run_every
        else:
            timeout=max(60,task.run_every/4)
            if tb:
                logging.error("Periodic task %s failed\n%s\n"%(unicode(task),tb))
        task.next_run=datetime.datetime.now()+datetime.timedelta(seconds=timeout)
        task.save()
        self.periodic_task_lock.acquire()
        try:
            del self.active_periodic_tasks[task.id]
        finally:
            self.periodic_task_lock.release()
    ##
    def on_new_connect(self):
        conn,addr=self.listener.accept()
        address,port=addr
        if Activator.objects.filter(ip=address).count()==0:
            logging.error("Refusing connection from %s"%address)
            socket.close(conn)
            return
        logging.info("Connect from: %s"%address)
        s=SAEStream(self.service,conn)
        self.streams.register(s)
        
    def on_stream_close(self,stream):
        self.streams.unregister(stream)
        
    def register_activator(self,name,stream):
        self.streams.register(stream,name)
        
    def get_activator_stream(self,name):
        try:
            return self.streams.get_stream(name)
        except:
            raise Exception("Activator not available: %s"%name)

    def pull_config(self,object):
        def pull_config_callback(transaction,response=None,error=None):
            if error:
                logging.error("pull_config failed: %s"%error.text)
                return
            object=Config.objects.get(id=transaction.object_id)
            if object.pull_every:
                object.next_pull=datetime.datetime.now()+datetime.timedelta(seconds=object.pull_every)
            object.write(response.config)
        stream=self.get_activator_stream(object.activator.name)
        r=PullConfigRequest()
        r.access_profile.profile           =object.profile_name
        r.access_profile.scheme            = object.scheme
        r.access_profile.address           = object.address
        if object.port:
            r.access_profile.port          = object.port
        if object.user:
            r.access_profile.user          = object.user
        if object.password:
            r.access_profile.password      = object.password
        if object.super_password:
            r.access_profile.super_password= object.super_password
        if object.remote_path:
            r.access_profile.path          = object.remote_path
        t=stream.proxy.pull_config(r,pull_config_callback)
        t.object_id=object.id
        