//---------------------------------------------------------------------
// cm.confdbquery application
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.cm.confdbquery.Application");

Ext.define("NOC.cm.confdbquery.Application", {
    extend: "NOC.core.ModelApplication",
    requires: [
        "NOC.cm.confdbquery.Model"
    ],
    model: "NOC.cm.confdbquery.Model",
    search: true,

    initComponent: function() {
        var me = this;

        me.jsonPanel = Ext.create("NOC.core.JSONPreview", {
            app: me,
            restUrl: new Ext.XTemplate('/cm/confdbquery/{id}/json/'),
            previewName: new Ext.XTemplate('ConfDB Query: {name}')
        });

        me.ITEM_JSON = me.registerItem(me.jsonPanel);

        Ext.apply(me, {
            columns: [
                {
                    text: __("Name"),
                    dataIndex: "name",
                    width: 150
                }
            ],

            fields: [
                {
                    name: "name",
                    xtype: "textfield",
                    fieldLabel: __("Name"),
                    labelAlign: "top",
                    allowBlank: false,
                    uiStyle: "medium"
                },
                {
                    name: "uuid",
                    xtype: "displayfield",
                    fieldLabel: __("UUID"),
                    labelAlign: "top",
                    allowBlank: true
                },
                {
                    name: "description",
                    xtype: "textarea",
                    fieldLabel: __("Description"),
                    labelAlign: "top",
                    allowBlank: true
                },
                {
                    name: "params",
                    xtype: "gridfield",
                    fieldLabel: __("Parameters"),
                    labelAlign: "top",
                    columns: [
                        {
                            dataIndex: "name",
                            text: __("Name"),
                            editor: "textfield",
                            width: 150
                        },
                        {
                            dataIndex: "type",
                            text: __("Type"),
                            width: 70,
                            editor: {
                                xtype: "combobox",
                                store: [
                                    ["str", "str"],
                                    ["int", "int"],
                                    ["bool", "bool"]
                                ]
                            }
                        },
                        {
                            dataIndex: "default",
                            text: __("Default"),
                            editor: "textfield",
                            width: 200
                        },
                        {
                            dataIndex: "description",
                            text: __("Description"),
                            editor: "textfield",
                            flex: 1
                        }
                    ]
                },
                {
                    xtype: "fieldset",
                    title: __("Allow"),
                    layout: "hbox",
                    defaults: {
                        padding: 4
                    },
                    items: [
                        {
                            name: "allow_object_filter",
                            xtype: "checkbox",
                            boxLabel: __("Object Filter")
                        },
                        {
                            name: "allow_object_validation",
                            xtype: "checkbox",
                            boxLabel: __("Object Validation")
                        },
                        {
                            name: "allow_interface_filter",
                            xtype: "checkbox",
                            boxLabel: __("Interface Filter")
                        },
                        {
                            name: "allow_interface_validation",
                            xtype: "checkbox",
                            boxLabel: __("Interface Validation")
                        }
                    ]
                },
                {
                    name: "require_raw",
                    xtype: "checkbox",
                    boxLabel: "Require raw"
                },
                {
                    name: "source",
                    xtype: "cmtext",
                    fieldLabel: __("Source"),
                    labelAlign: "top",
                    allowBlank: false,
                    mode: "python"
                }
            ],

            formToolbar: [
                {
                    text: __("JSON"),
                    glyph: NOC.glyph.file,
                    tooltip: __("Show JSON"),
                    hasAccess: NOC.hasPermission("read"),
                    scope: me,
                    handler: me.onJSON
                }
            ]

        });
        me.callParent();
    },

    //
    onJSON: function() {
        var me = this;
        me.showItem(me.ITEM_JSON);
        me.jsonPanel.preview(me.currentRecord);
    }
});
