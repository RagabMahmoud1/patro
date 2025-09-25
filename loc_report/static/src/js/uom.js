odoo.define('loc_report.loc', function (require) {
    'use strict';
    var core = require('web.core');
    var QWeb = core.qweb;
    var AbstractAction = require('web.AbstractAction');
    var uom_report_view = AbstractAction.extend({
        hasControlPanel: true,


        init: function (parent, action) {
            $(".main_report").empty();
            this.report_name = action.report_name;
            this.lines = action.lines;
            this.cloumns = action.cloumns;
            this.locs = action.locs;
            return this._super.apply(this, arguments);

        },


        renderElement: function () {
            this._super();
            var self = this;
            var lines = [];
            var cloumns = [];
            var locs = [];
            if (this.lines) {
                for (var i in this.lines) {
                    lines.push(this.lines[i]);
                }

            }

            if (this.cloumns) {
                for (var i in this.cloumns) {
                    cloumns.push(this.cloumns[i]);
                }

            }
            if (this.locs) {
                for (var i in this.locs) {
                    locs.push(this.locs[i]);
                }

            }

            var $content = $(QWeb.render("report_uom", {
                heading: self.report_name,
                id: self.id,
                type: 'report',
                lines: lines,
                cloumns: cloumns,
                locs: locs,
                group: this.group
            }));
            self.$el.html($content);
            return;
        },


    });


    core.action_registry.add("uom_report_view", uom_report_view);
    return top_vendor_view;
});