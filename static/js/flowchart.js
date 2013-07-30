jsPlumb.ready(function() {
		jsPlumb.importDefaults({
			Container: $('#semiconductor-flowchart'),
			DragOptions : { cursor: 'pointer', zIndex:2000 },
			EndpointStyles : [{ fillStyle:'#225588' }, { fillStyle:'#225588' }],
			Endpoints : [ [ "Dot", {radius:3} ], [ "Dot", { radius:3 } ]],
			ConnectionOverlays : [
				[ "PlainArrow", { location:1.0, width:5, length: 8}],
			]
		});	
			
		var connectorPaintStyle = {
				lineWidth:1,
				strokeStyle:"#333333",
				joinstyle:"round",
		};
		
		var connectorHoverStyle = {
				lineWidth:1,
				strokeStyle:"#2e2aF8"
		};
			
		var	sourceEndpoint = {
				endpoint:"Dot",
				paintStyle:{ fillStyle:"#558822",radius:1 },
				isSource:true,
				connector:[ "StateMachine"],								                
				connectorStyle:connectorPaintStyle,
				hoverPaintStyle:connectorHoverStyle,
				connectorHoverStyle:connectorHoverStyle,
                dragOptions:{},
		};
		
		var	flowSourceEndpoint = {
				endpoint:"Dot",
				paintStyle:{ fillStyle:"#558822",radius:1 },
				isSource:true,
				connector:[ "Flowchart", {gap:0.5, stub:5} ],								                
				connectorStyle:connectorPaintStyle,
				hoverPaintStyle:connectorHoverStyle,
				connectorHoverStyle:connectorHoverStyle,
                dragOptions:{},
		};

		var targetEndpoint = {
				endpoint:"Dot",					
				paintStyle:{ fillStyle:"#00ffff",radius:1 },
				hoverPaintStyle:connectorHoverStyle,
				maxConnections:-1,
				dropOptions:{ hoverClass:"hover", activeClass:"active" },
				isTarget:true,			
		};
		
		var allSourceEndpoints = [], allTargetEndpoints = [];
		_addEndpoints = function(toId, sourceAnchors, targetAnchors, flowSourceAnchors) {
			for (var i = 0; i < sourceAnchors.length; i++) {
				var sourceUUID = toId + "-" + sourceAnchors[i];
				allSourceEndpoints.push(jsPlumb.addEndpoint(toId, sourceEndpoint, { anchor:sourceAnchors[i], uuid:sourceUUID }));						
			}
			for (var k = 0; k < flowSourceAnchors.length; k++) {
				var flowSourceUUID = toId + "-" + flowSourceAnchors[k];
				allSourceEndpoints.push(jsPlumb.addEndpoint(toId, flowSourceEndpoint, { anchor:flowSourceAnchors[k], uuid:flowSourceUUID }));						
			}
			for (var j = 0; j < targetAnchors.length; j++) {
				var targetUUID = toId + "-" + targetAnchors[j];
				allTargetEndpoints.push(jsPlumb.addEndpoint(toId, targetEndpoint, { anchor:targetAnchors[j], uuid:targetUUID }));						
			}
		};

		_addEndpoints("electronic-products-node", ["RightMiddle"], ["BottomCenter"], []);
		_addEndpoints("distribution-of-electronic-products-node", [], ["LeftMiddle"], []);
		
		_addEndpoints("distributors-node", ["RightMiddle"], ["BottomCenter"], []);
		_addEndpoints("electronic-manufacturing-services-node", ["TopCenter"], ["BottomCenter", "LeftMiddle", "RightMiddle"], []);
		_addEndpoints("circuit-boards-node", ["LeftMiddle"], [], []);
		
		_addEndpoints("semiconductors-node", ["TopCenter"], ["BottomCenter"], ["TopRight"]);
		_addEndpoints("displays-screens-node", [], [], ["TopCenter"]);
		_addEndpoints("wiring-connectors-keyboards-node", [], [], ["TopCenter"]);
		_addEndpoints("cases-node", [], [], ["TopCenter"]);
		_addEndpoints("hard-drives-node", [], [], ["TopCenter"]);
		
		_addEndpoints("assembly-and-test-node", ["TopCenter"], ["RightMiddle"], []);
		_addEndpoints("semiconductor-fabrication-node", ["LeftMiddle"], ["RightMiddle", "BottomCenter"], []);
		_addEndpoints("idm-and-fabless-company-circuit-design-node", ["LeftMiddle"], [], []);
		
		_addEndpoints("process-tools-node", [], ["BottomCenter"], ["TopCenter"]);
		_addEndpoints("process-chemicals-node", [], [], ["TopCenter"]);
		_addEndpoints("wafers-node", [], [], ["TopCenter"]);
		_addEndpoints("masks-node", [], [], ["TopCenter"]);
		_addEndpoints("component-suppliers-node", ["TopCenter"], [], []);
		
		jsPlumb.connect({uuids:["electronic-products-node-RightMiddle", "distribution-of-electronic-products-node-LeftMiddle"], editable:false});
		jsPlumb.connect({uuids:["electronic-manufacturing-services-node-TopCenter", "electronic-products-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["distributors-node-RightMiddle", "electronic-manufacturing-services-node-LeftMiddle"], editable:false});
		jsPlumb.connect({uuids:["circuit-boards-node-LeftMiddle", "electronic-manufacturing-services-node-RightMiddle"], editable:false});
		
		jsPlumb.connect({uuids:["semiconductors-node-TopCenter", "distributors-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["semiconductors-node-TopRight", "electronic-manufacturing-services-node-BottomCenter"], editable:false,});
		jsPlumb.connect({uuids:["displays-screens-node-TopCenter", "electronic-manufacturing-services-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["wiring-connectors-keyboards-node-TopCenter", "electronic-manufacturing-services-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["cases-node-TopCenter", "electronic-manufacturing-services-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["hard-drives-node-TopCenter", "electronic-manufacturing-services-node-BottomCenter"], editable:false});
		
		jsPlumb.connect({uuids:["assembly-and-test-node-TopCenter", "semiconductors-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["semiconductor-fabrication-node-LeftMiddle", "assembly-and-test-node-RightMiddle"], editable:false});
		jsPlumb.connect({uuids:["idm-and-fabless-company-circuit-design-node-LeftMiddle", "semiconductor-fabrication-node-RightMiddle"], editable:false});
		
		
		jsPlumb.connect({uuids:["process-tools-node-TopCenter", "semiconductor-fabrication-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["process-chemicals-node-TopCenter", "semiconductor-fabrication-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["wafers-node-TopCenter", "semiconductor-fabrication-node-BottomCenter"], editable:false});
		jsPlumb.connect({uuids:["masks-node-TopCenter", "semiconductor-fabrication-node-BottomCenter"], editable:false});
		
		jsPlumb.connect({uuids:["component-suppliers-node-TopCenter", "process-tools-node-BottomCenter"], editable:false});
});	