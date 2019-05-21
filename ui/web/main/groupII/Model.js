//---------------------------------------------------------------------
// main.group Model
//---------------------------------------------------------------------
// Copyright (C) 2007-2019 The NOC Project
// See LICENSE for details
//---------------------------------------------------------------------
console.debug("Defining NOC.main.groupII.Model");

Ext.define("NOC.main.groupII.Model", {
    extend: "Ext.data.Model",
    rest_url: "/main/groupII/",

    fields: [
        {
            name: "id",
            type: "string"
        },
        {
            name: "name",
            type: "string"
        },
        {
            name: "permissions",
            type: "auto"
        }
    ]
});