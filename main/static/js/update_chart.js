let projects = [];
let stub = null;

function updateSuccess (data) {
    projects[data.arr_id].percent = data.percent;
    projects[data.arr_id].arr_id = data.arr_id;
    projects[data.arr_id].selfUpdate = selfUpdateFunc;
}

function selfUpdateFunc() {
    $.get(`/api/v1/update_project/${this.pk}/${this.arr_id}/`, updateSuccess);
}

function unratedStatusSuccess (data) {
    data.forEach(element => {
        if (projects.some(e => e.pk === element.pk)){} 
        else {
            element.arr_id = projects.length;
            element.selfUpdate = selfUpdateFunc;
            projects.push(element);
        }
    });
    projects.sort((a, b) => { a.percent - b.percent });
}

function updateChart () {
    $.get("/api/v1/unrated_status/", unratedStatusSuccess);
    let labelsArray = [];
    let percentsArray = [];
    for (let i=0; i<projects.length; i++){
        projects[i].selfUpdate();
        labelsArray.push(projects[i].name);
        percentsArray.push(projects[i].percent);
    }
    onlineChart.data.labels = labelsArray;
    onlineChart.data.datasets[0].data = percentsArray;
    onlineChart.update();

}
updateChart();
setInterval(updateChart, 10000);