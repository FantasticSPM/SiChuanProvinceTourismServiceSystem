const os=require('os');

function getip(){
	let needhost="";
	try {
		let network=os.networkInterfaces();
		for(let dev in network){
			let iface=network[dev];
			for (let i=0;i<iface.length;i++){
				let alias=iface[i];
				if(alias.family==='IPv4'&&alias.address!=='127.0.0.1'&&!alias.internal){
					needhost=alias.address;
				}
			}
		}
	}catch(e){
		needhost='localhost';
	}
	return needhost
}

export default getip()