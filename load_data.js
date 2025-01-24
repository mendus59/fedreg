function getLatestDate(data) {
   // convert to timestamp and sort
   var sorted_ms = data.map(function(item) {
      return new Date(item.publication_date).toDateString()
   }).sort(); 
   // take latest
   var latest_ms = sorted_ms[sorted_ms.length-1];
   // convert to js date object 
   return new Date(latest_ms).toUTCString();
}

async function load_data(){
    var data = {
        objects:[]
    };
    const response = await fetch("./logs/write_log.txt");
    const log_data = await response.text();
    const lines = log_data.split("\n");

    for(let i = 0; i < lines.length; i++){
        await fetch(lines[i])
            .then((response) => response.json())
            .then((json) => data.objects.push(json))
    }
    
    data.objects.sort((a, b) => b.publication_date.localeCompare(a.publication_date))
    data.latest_date = getLatestDate(data.objects).toString()
    var exec_orders = Handlebars.compile(document.querySelector("#exec_orders").innerHTML);
    var loaded = exec_orders(data);
    document.querySelector("#content").innerHTML = loaded;
}
