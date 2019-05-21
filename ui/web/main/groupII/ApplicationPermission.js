//---------------------------------------------------------------------
// main.group Appliction Permissions widget
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.groupII.ApplicationPermission");

Ext.define("NOC.main.groupII.ApplicationPermission", {
    extend: "Ext.panel.Panel",
    alias: "widget.noc.groupII.applicationperm",
    defaultListenerScope: true,
    bodyPadding: 5,
    collapsed: true,
    border: false,
    tpl: new Ext.XTemplate(
        '<dl>',
        '<tpl foreach=".">',
        '<dt><b>{title} ({$})</b>',
        '<dd style="display: flex;flex-wrap: wrap; margin-bottom: 10px;">',
        '<tpl for="perms">',
        '<div id="checkbox-{id}" class="x-form-type-checkbox <tpl if="status">x-form-cb-checked"</tpl>" style="margin-right: 20px;">',
        '<div id="checkbox-{id}-bodyEl" class="x-form-item-body x-form-item-body-default x-form-cb-wrap x-form-cb-wrap-default">',
        '<div id="checkbox-{id}-innerWrapEl" class="x-form-cb-wrap-inner">',
        '<input id="checkbox-{id}-inputEl" data-perm="{id}" class="x-form-cb-input x-hidden-clip">',
        '<span id="checkbox-{id}-displayEl" data-perm="{id}"',
        'class="x-form-field x-form-checkbox x-form-checkbox-default x-form-cb x-form-cb-default"></span>',
        '<label id="checkbox-{id}-boxLabelEl" class="x-form-cb-label x-form-cb-label-default x-form-cb-label-after"',
        'for="checkbox-{id}-inputEl">{name}</label>',
        '</div>',
        '</div>',
        '</div>',
        '</tpl>',
        '</dd>',
        '</dt>',
        '</tpl>',
        '</dl>'
    ),
    listeners: {
        element: "el",
        click: "eventLoop",
        delegate: "div.x-form-type-checkbox"
    },
    tools: [
        {
            type: "refresh",
            tooltip: __("Reset title permissions"),
            callback: "resetPermission"
        },
        {
            type: "expand",
            itemId: "expandTool",
            callback: "togglePanel"
        }
    ],
    eventLoop: function(evt) {
        var element;
        // checkbox clicked
        element = evt.getTarget("[data-perm]", 1, true);
        if(element) {
            this.setPermission(element.getAttribute("data-perm"));
        }
    },
    setPermission: function(value) {
        var data = this.getData(),
            tokens = value.split("-"),
            title = tokens[1];
        Ext.each(data[title].perms, function(p) {
            if(p.id === value) {
                p.status = !p.status;
                return false;
            }
        });
        this.setData(data);
    },
    resetPermission: function() {
        var data = this.getData();
        Ext.Object.each(data, function(name, app) {
            Ext.each(app.perms, function(perm) {
                perm.status = false;
            });
        });
        this.setData(data);
    },
    togglePanel: function(panel) {
        var tool = panel.query("[itemId=expandTool]")[0];
        panel.toggleCollapse();
        tool.setType(tool.type === "expand" ? "collapse" : "expand");
    }
});