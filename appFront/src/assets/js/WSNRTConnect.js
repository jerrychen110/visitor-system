
export const WSNRTConnect = function(myZCloudID, myZCloudKey) {
	var thiz = this;
	thiz.uid = myZCloudID;
	thiz.key = myZCloudKey;
	thiz.saddr = "api.zhiyun360.com:28090";
	
	thiz.onConnect = null;
	thiz.onConnectLost = null;
	thiz.onmessageArrive = null;

	thiz.setIdKey = function(uid, key) {
		thiz.uid = uid;
		thiz.key = key;		
	};
	
	thiz.initZCloud = function(uid, key) {
		thiz.uid = uid;
		thiz.key = key;		
	};
	
	thiz.setServerAddr = function(addr) {
		thiz.saddr = addr;
	};
	
	thiz.disconnect = function() {
		if (thiz.wsc) {
			thiz.wsc.close();
		}
	};
	thiz.connect = function() {
		thiz.wsc = new WebSocket('wss://'+thiz.saddr);
		thiz.wsc.onopen = function(event) {
			var auth = {
				method:"authenticate",
				uid:thiz.uid,
				key:thiz.key		
			};
			var dat = JSON.stringify(auth);
			thiz.wsc.send(dat);	
			if (thiz.onConnect) thiz.onConnect();
		};
		thiz.wsc.onmessage = function(message) {
			//try{
				var msg = JSON.parse(message.data);
				if (msg.method && msg.addr && msg.data) {
					if (msg.method == 'message') {
						if (thiz.onmessageArrive) thiz.onmessageArrive(msg.addr, msg.data);
					}
				}
			//} catch (err) {
			//	console.log("error msg "+err);
			//}
		};
		thiz.wsc.onclose = function() {
			if (thiz.onConnectLost) thiz.onConnectLost();
		};
	};
	
	thiz.sendMessage = function(mac, payload) {
		var msg = {
				method:"control",
				addr:mac,
				data:payload
		};
		var dat = JSON.stringify(msg);
		thiz.wsc.send(dat);
	};
};
