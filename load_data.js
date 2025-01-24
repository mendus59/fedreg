function getLatestDate(data) {
   // convert to timestamp and sort
   var sorted_ms = data.map(function(item) {
      return item.publication_date
   }).sort(); 
   // take latest
   var latest_ms = sorted_ms[sorted_ms.length-1];
   // convert to js date object 
   return latest_ms;
}

async function load_data(){
    var data = {
        objects:[]
    };
    const response = await fetch("./logs/write_log.txt");
    const log_data = await response.text();
    const lines = log_data.split("\n");

    for(let i = 0; i < lines.length; i++){
        try {
            object = await fetch(lines[i])
            json_object = await object.json()
            await data.objects.push(json_object)
        } catch (error) {
            console.log(error)
            console.log(json_object)
        }
    }
    data.objects.sort((a, b) => b.publication_date.localeCompare(a.publication_date))
    data.latest_date = getLatestDate(data.objects).toString()
    var exec_orders = Handlebars.compile(document.querySelector("#exec_orders").innerHTML);
    var loaded = exec_orders(data);
    document.querySelector("#content").innerHTML = loaded;
}
