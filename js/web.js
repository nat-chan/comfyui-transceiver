//import { app } from "../../scripts/app.js";
//import { api } from "../../scripts/api.js";
//
//app.registerExtension({
//    name: "MyCustomNodes",
//    async beforeRegisterNodeDef(nodeType, nodeData, app) {
//        if (nodeData.name === "TextInput") {
//            const origOnNodeCreated = nodeType.prototype.onNodeCreated;
//            nodeType.prototype.onNodeCreated = function () {
//                const r = origOnNodeCreated ? origOnNodeCreated.apply(this) : undefined;
//                for (const w of this.widgets) {
//                    if (w.name === "seed") {
//                        w.type = "converted-widget";
//                        if (!w.linkedWidgets) continue;
//                        for (const lw of w.linkedWidgets) {
//                            lw.type = "converted-widget";
//                        }
//                    }
//                }
//                return r;
//            }
//
//            nodeType.prototype.color = LGraphCanvas.node_colors.green.color;
//            nodeType.prototype.bgcolor = LGraphCanvas.node_colors.green.bgcolor;
//        }
//        else if (nodeData.name === "TextOutput") {
//            nodeType.prototype.color = LGraphCanvas.node_colors.green.color;
//            nodeType.prototype.bgcolor = LGraphCanvas.node_colors.green.bgcolor;
//        }
//    }
//})