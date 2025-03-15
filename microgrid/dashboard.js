let ajaxURL = '/energy-dashboard/inc/ajax.php';
let buildingImagesURL = '/energy-dashboard/assets/images/buildings/';


function getAjax ( url, success ) {
    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    xhr.open('GET', url);
    xhr.onreadystatechange = function() {
        if ( xhr.readyState > 3 && xhr.status == 200 ) success(xhr.responseText);
    };
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.send();
    return xhr;
}


document.addEventListener("DOMContentLoaded", function() {
    
    console.log('Document Ready!');
    
    new Promise((resolve, reject) => {
        getAjax(ajaxURL+'?overview=true', function(data){
            resolve(JSON.parse(data));
        });
    }).then((response) => {
        
        let container = document.getElementById('aggregatedConsumption');
        container.innerHTML = '<p><em>Data representing: '+response.data.date+'</p>';
        container.innerHTML += '<canvas></canvas>';
        container.innerHTML += '<p><em>Segment data by selecting a label in the chart legend above.</em><br /><em>Units: Gigajoules (GJ)</em></p>';
        
        let cooling = [];
        let heating = [];
        let electrical = [];
        
        Object.keys(response.data.buildings).forEach(b => {
            cooling.push(response.data.buildings[b].cooling);
            heating.push(response.data.buildings[b].heating);
            electrical.push(response.data.buildings[b].electrical);
        });
        
        charts = new Chart(container.querySelector('canvas'), {
            type: 'bar',
            data: {
                labels: response.data.labels,
                 datasets: [
                    {
                        label: 'Cooling',
                        data: cooling,
                        backgroundColor: ['#0085ca']
                    },
                    {
                        label: 'Heating',
                        data: heating,
                        backgroundColor: ['#c8102e']
                    },
                    {
                        label: 'Electrical',
                        data: electrical,
                        backgroundColor: ['#009a44']
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                },
                scales: {
                    x: { stacked: true },
                    y: { stacked: true }
                }
            }
        });
    });
    
    
    new Promise((resolve, reject) => {
        getAjax(ajaxURL+'?overview_intesity=true', function(data){
            resolve(JSON.parse(data));
        });
    }).then((response) => {
        
        let container = document.getElementById('aggregatedEnergyIntensity');
        container.innerHTML = '<p><em>Data representing: '+response.data.date+'</p>';
        container.innerHTML += '<canvas></canvas>';
        container.innerHTML += '<p><em>Units: Gigajoules (GJ)</em></p>'; 
        
        let values = [];
        let labels = [];
        
        Object.keys(response.data.buildings).forEach(b => {
            values.push(response.data.buildings[b].value);
            labels.push(b.toUpperCase());
        });
        
        charts = new Chart(container.querySelector('canvas'), {
            type: 'bar',
            data: {
                labels: labels,
                 datasets: [
                    {
                        label: 'Consumption Ranking in GJ / 1,000 Square Meters',
                        data: values,
                        backgroundColor: ['#00502E']
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                },
                scales: {
                    x: { stacked: true },
                    y: { stacked: true }
                }
            }
        });
    });
    
    // https://gomakethings.com/how-to-test-if-an-element-is-in-the-viewport-with-vanilla-javascript/
    
    let buildingGraphs = document.querySelectorAll('div[data-building]');
    buildingGraphs.forEach((b) => {
        
        let buildingCode = b.dataset.building;
        
        b.innerHTML = '<div class="tw-grid tw-gap-8 md:tw-grid-cols-2"><div id="'+buildingCode+'_consuption"><svg xmlns="http://www.w3.org/2000/svg" class="tw-m-auto tw-block" height="200px" preserveaspectratio="xMidYMid" viewbox="0 0 100 100" width="200px"> <rect fill="#014f2e" height="55" width="13" x="18.5" y="22.5"> <animate attributename="y" begin="-0.21052631578947367s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="0.5;22.5;22.5"/> <animate attributename="height" begin="-0.21052631578947367s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="99;55;55"/> </rect> <rect fill="#014f2e" height="55" width="13" x="43.5" y="22.5"> <animate attributename="y" begin="-0.10526315789473684s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="6;22.5;22.5"/> <animate attributename="height" begin="-0.10526315789473684s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="88;55;55"/> </rect> <rect fill="#014f2e" height="55" width="13" x="68.5" y="22.5"> <animate attributename="y" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="6;22.5;22.5"/> <animate attributename="height" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="88;55;55"/></rect></svg></div><div id="'+buildingCode+'_greenhouse"><svg xmlns="http://www.w3.org/2000/svg" class="tw-m-auto tw-block" height="200px" preserveaspectratio="xMidYMid" viewbox="0 0 100 100" width="200px"> <rect fill="#014f2e" height="55" width="13" x="18.5" y="22.5"> <animate attributename="y" begin="-0.21052631578947367s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="0.5;22.5;22.5"/> <animate attributename="height" begin="-0.21052631578947367s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="99;55;55"/> </rect> <rect fill="#014f2e" height="55" width="13" x="43.5" y="22.5"> <animate attributename="y" begin="-0.10526315789473684s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="6;22.5;22.5"/> <animate attributename="height" begin="-0.10526315789473684s" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="88;55;55"/> </rect> <rect fill="#014f2e" height="55" width="13" x="68.5" y="22.5"> <animate attributename="y" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="6;22.5;22.5"/> <animate attributename="height" calcmode="spline" dur="1.0526315789473684s" keysplines="0 0.5 0.5 1;0 0.5 0.5 1" keytimes="0;0.5;1" repeatcount="indefinite" values="88;55;55"/></rect></svg></div></div>';
        
        // Load Consumption Data for Building
        new Promise((resolve, reject) => {
            getAjax(ajaxURL+'?building_rankings='+buildingCode+'&type=consuption', function(data){
                resolve(JSON.parse(data));
            });
        }).then((response) => {
            
            let bc = document.getElementById(buildingCode+'_consuption');
            
            bc.innerHTML = '<h3>Aggregated Consumption Rankings</h3>';
            bc.innerHTML += '<p><em>Data representing: '+response.data.date+'</em></p>';
            bc.innerHTML += '<canvas class="chart" data-graph="consumption" data-building="'+buildingCode+'"></canvas>';
            bc.innerHTML += '<p><em>Segment data by selecting a label in the chart legend above.<br />Units: Gigajoules (GJ)</em></p>';
            
            const data = {
                labels: response.data.labels,
                datasets: [
                    {
                        label: 'Cooling',
                        data: response.data.cooling,
                        backgroundColor: ['#0085ca']
                    },
                    {
                        label: 'Heating',
                        data: response.data.heating,
                        backgroundColor: ['#c8102e']
                    },
                    {
                        label: 'Electrical',
                        data: response.data.electrical,
                        backgroundColor: ['#009a44']
                    }
                ]
            };
            const config = {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    },
                    scales: {
                        x: { stacked: true },
                        y: { stacked: true }
                    }
                }
            };
            
            let chart = new Chart(document.querySelector('canvas[data-graph="consumption"][data-building="'+buildingCode+'"]'), config);
        });
        
        // Load Greenhouse Data for Building
        new Promise((resolve, reject) => {
            getAjax(ajaxURL+'?building_rankings='+buildingCode+'&type=greenhouse', function(data){
                resolve(JSON.parse(data));
            });
        }).then((response) => {
            
            let bc = document.getElementById(buildingCode+'_greenhouse');
            
            bc.innerHTML = '<h3>Greenhouse Gas Rankings</h3>';
            bc.innerHTML += '<p><em>Data representing: '+response.data.date+'</em></p>';
            bc.innerHTML += '<canvas class="chart" data-graph="greenhouse" data-building="'+buildingCode+'"></canvas>';
            bc.innerHTML += '<p><em>Segment data by selecting a label in the chart legend above.<br />Units: Gigajoules (GJ)</em></p>';
            
            // Draw Graph
            const data = {
                labels: response.data.labels,
                datasets: [
                    {
                        label: 'Cooling',
                        data: response.data.cooling,
                        backgroundColor: ['#0085ca']
                    },
                    {
                        label: 'Heating',
                        data: response.data.heating,
                        backgroundColor: ['#c8102e']
                    },
                    {
                        label: 'Electrical',
                        data: response.data.electrical,
                        backgroundColor: ['#009a44']
                    }
                ]
            };
            const config = {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    },
                    scales: {
                        x: { stacked: true },
                        y: { stacked: true }
                    }
                }
            };
            
            let chart2 = new Chart(document.querySelector('canvas[data-graph="greenhouse"][data-building="'+buildingCode+'"]'), config);
        });
        
    });
    
    
    // Display Todays Consumption by Building
    let todaysConsumption = document.getElementById('todays_consumption');
    new Promise((resolve, reject) => {
        getAjax(ajaxURL+'?todays_consumption', function(data){
            resolve(JSON.parse(data));
        });
    }).then((response) => {
        
        todaysConsumption.innerHTML = response.data.description;
        todaysConsumption.innerHTML += '<div class="buildings tw-grid tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-6"></div>';
        
        let buildingsContainer = todaysConsumption.querySelector('.buildings');
        let todayCharts = [];
        
        Object.keys(response.data.buildings).forEach((b) => {
            let building = response.data.buildings[b];
            buildingsContainer.innerHTML += '<div id="building_'+b+'" class="tw-shadow"><div class="tw-object-cover tw-h-52 tw-z-0 tw-relative"><img class="tw-w-full tw-h-full" src="'+buildingImagesURL+b+'.jpg" alt="'+building.name+'" /></div><div class="tw-block tw-relative tw-bg-white tw-mx-4 tw--mt-10 tw-p-3 tw-z-10"><h3>'+building.name+'</h3><div class="tw-mt-3 tw-relative"><div class="total total tw-absolute tw-w-full tw-text-center tw-top-1/2 tw--mt-12 tw-text-base sm:tw-text-3xl lg:tw-text-4xl"></div><canvas id="'+b+'Chart"></canvas></div><p class="tw-text-center tw-mt-3 tw-italic">Units: Gigajoules (GJ)</p></div></div>';
        });
        
        Object.keys(response.data.buildings).forEach((b) => {
            let building = response.data.buildings[b];
            document.querySelector('#building_'+b+' .total').innerHTML = building.total;
            todayCharts[b] = new Chart(document.querySelector('#building_'+b+' canvas'), {
                type: 'doughnut',
                data: {
                    labels: ['Cooling', 'Heating', 'Electrical'],
                    datasets: [{
                        data: [building.cooling, building.heating, building.electrical],
                        backgroundColor: ['#0085ca', '#c8102e', '#009a44'],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        });
    });

});