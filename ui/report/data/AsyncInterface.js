// Generated by CoffeeScript 1.10.0
(function() {
  Ext.define('Report.data.AsyncInterface', {
    config: {
      success: Ext.emptyFn,
      failure: Ext.emptyFn,
      always: Ext.emptyFn,
      scope: null
    },
    constructor: function(config) {
      this.initConfig(config);
      return this.setScope(this.getScope || this);
    },
    callSuccess: function() {
      var scope;
      scope = this.getScope();
      this.getSuccess().apply(scope, arguments);
      this.callAlways.apply(scope, arguments({
        callFailure: function() {}
      }));
      scope = this.getScope();
      this.getFailure().apply(scope, arguments);
      this.callAlways.apply(scope, arguments({
        callAlways: function() {}
      }));
      return this.getAlways().apply(this.getScope(), arguments);
    }
  });

}).call(this);

//# sourceMappingURL=AsyncInterface.js.map
