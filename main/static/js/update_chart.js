let projects = [];

function unratedStatusSuccess (data) {
    console.log(data);
    data.forEach(element => {
        if (projects.some(e => e.pk === element.pk)){} 
        else {
            projects.push(element);
        }
    });
    projects.sort((a, b) => { a.percent - b.percent });
}

function updateChart () {
    $.get("/api/v1/unrated_status/", unratedStatusSuccess);
    let labelsArray = [];
    let percentsArray = []
    for (let i=0; i<projects.length; i++){
        labelsArray.push(projects[i].name);
        percentsArray.push(projects[i].percent);
    }
    onlineChart.data.labels = labelsArray;
    onlineChart.data.datasets[0].data = percentsArray;
    onlineChart.update();

}
updateChart();
setInterval(updateChart, 10000);