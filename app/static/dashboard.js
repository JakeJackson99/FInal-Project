loadItems();


/**
 * Makes a request to /.../chart_data, receives an object, and implements its contents into the charts.
 * It creats an instance of a chart and adds it to #time-chart.
 */
function loadItems() {
    fetch('/dashboard/chart_data').then(response => response.json()).then(data => {
        var page_time = document.getElementById('time-chart').getContext('2d');
        var gender_time = document.getElementById('gender-time-chart').getContext('2d');

        var chart = new Chart(page_time, {
            type: 'bar',

            data: {
                labels: ['Endless', 'Discrete'],
                datasets: [{
                    label: 'Average Time Spent on Each Type of Page',
                    backgroundColor: 'rgb(75, 122, 0)',
                    data: [data["endless_time"], data["discrete_time"], 0]
                }],
            },

            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMax: 24,
                            suggestedMin: 0,
                            stepSize: 3
                        }
                    }]
                }
            }
        });

        var chart = new Chart(gender_time, {
            type: 'bar',

            data: {
                labels: ['Male', 'Female'],
                datasets: [{
                    label: 'Average Gender Time Spent Scrolling',
                    backgroundColor: 'rgb(0, 67, 125)',
                    data: [data["male_time"], data["female_time"], 0]
                }]
            },

            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMax: 24,
                            suggestedMin: 0,
                            stepSize: 3
                        }
                    }]
                }
            }
        });
    });
}
