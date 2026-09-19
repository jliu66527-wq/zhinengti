function createDetailRequestGate(){let latestRequest=0;return{begin:()=>(latestRequest+=1,latestRequest),isCurrent:requestId=>requestId===latestRequest}}export{createDetailRequestGate as c};
