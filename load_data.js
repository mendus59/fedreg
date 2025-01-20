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
    var exec_orders = Handlebars.compile(document.querySelector("#exec_orders").innerHTML);
    var loaded = exec_orders(data);
    document.querySelector("#content").innerHTML = loaded;
}
