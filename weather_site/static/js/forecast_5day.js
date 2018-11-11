// ---------- Line chart Dimensions --------------- //
//Width and height
var margin = {top: 50, right: 50, bottom: 100, left: 50},
    w = 900 - margin.left - margin.right,
    h = 375 - margin.top - margin.bottom;

// --------------------------------------------------------------------------//
// ---------- Helper Functions ---------- //

//For converting strings to Dates
var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S%Z");

//For converting Dates to strings
//formatHour = d3.timeFormat("%I:%M %p")
var formatTime = d3.timeFormat("%a %I:%M %p"),
    formatHour = d3.timeFormat("%I %p"),
    formatDay = d3.timeFormat("%a"),
    bisectDate = d3.bisector(function(d) { return d.date_t; }).left;

  // ------------------------------------------------------------------------//
  // ---------- Load in data and create dataset ---------- //
    //Load in the data
function draw_forecast(data) {
// d3.json("static/js/la_forecast.json", function(data) {
// function draw_forecast(data) {

        var dataset = data.temperature.sched.map(parseTime).map(function(x, i) {
            return {'date_t':x,
                    'temp':data.temperature.values[i],
                    'date_h':data.humidity.sched.map(parseTime)[i],
                    'humidity': data.humidity.values[i],
                    'date_wd': data.direction.sched.map(parseTime)[i],
                    'direction': data.direction.values[i],
                    'date_ws': data.windSpeed.sched.map(parseTime)[i],
                    'wind_speed': data.windSpeed.values[i],
                    'date_cc': data.cloudCover.sched.map(parseTime)[i],
                    'cloudCover': data.cloudCover.values[i]
                  };
        });
        // Create a separate object for precipitation probabilities
        // which are reported on a different schedule
        var precips = data.precipProb.sched.map(parseTime).map(function(x, i) {
            return {'date_pp': x,
                    'precipProb': data.precipProb.values[i]
                    };
        });
        // Join precipitation data to full dataset
        dataset.forEach(function(datapoint) {
            var result = precips.filter(function(ppoint) {
                  return ppoint.date_pp.getTime() === datapoint.date_t.getTime();
            });
            datapoint.precipProb = (result[0] !== undefined) ? result[0].precipProb : null;
            datapoint.date_pp = (result[0] !== undefined) ? result[0].date_pp : null;
        });

        // console.log(dataset)
// --------------------------------------------------------------------------//
// TEMPERATURE AND HUMIDITY LINE CHART
// --------------------------------------------------------------------------//

        var min_temp = dataset.reduce((min, b) => Math.min(min, b.temp), dataset[0].temp);
        var max_temp = dataset.reduce((min, b) => Math.max(min, b.temp), dataset[0].temp);

        var min_ws = dataset.reduce((min, b) => Math.min(min, b.wind_speed), dataset[0].wind_speed);
        var max_ws = dataset.reduce((min, b) => Math.max(min, b.wind_speed), dataset[0].wind_speed);

        // SCALE FUNCTIONS
        var xScale_t = d3.scaleTime()
                 .domain([
                  d3.min(dataset, function(d) { return d.date_t; }),
                  d3.max(dataset, function(d) { return d.date_t; })
                ])
                 .range([0, w]);

        var xScale_h = d3.scaleTime()
                  .domain([
                   d3.min(dataset, function(d) { return d.date_h; }),
                   d3.max(dataset, function(d) { return d.date_h; })
                 ])
                  .range([0, w]);

        var yScale_t = d3.scaleLinear()
                 .domain([min_temp*.90, max_temp*1.1])
                 // .domain([5.4, 30])
                 .range([h, 0]);

        var yScale_h = d3.scaleLinear()
                  .domain([0, 100])
                  .range([h, 0]);

        var arcScale = d3.scaleLinear()
                  .domain([
                    d3.min(dataset, function(d) { return d.wind_speed; }),
                    d3.max(dataset, function(d) { return d.wind_speed; })
                  ])
                  .range([0, wind_w/2]);

        // CREATE AXES
        // Primary X Axis with hours
        var xAxis_hour = d3.axisBottom()
              .scale(xScale_t)
              .ticks(d3.timeHour.every(3))
              .tickSize(0)
              .tickFormat(formatHour);

        // Secondary X Axis with weekday
        var xAxis_day = d3.axisBottom()
              .scale(xScale_t)
              .ticks(d3.timeDay.every(1))
              .tickSize(0)
              .tickFormat(formatDay);

        // Left axis for temperature
        var yAxis_left = d3.axisLeft()
              .scale(yScale_t)
              .tickSize(0)
              .ticks(10);

        // Right axis for humidity
        var yAxis_right = d3.axisRight()
              .scale(yScale_h)
              .tickSize(0)
              .ticks(10);

        // Line generators and create svg
        var line_t = d3.line()
              .x(function(d) { return xScale_t(d.date_t); })
              .y(function(d) { return yScale_t(d.temp); });

        var line_h = d3.line()
              .x(function(d) { return xScale_t(d.date_h); })
              .y(function(d) { return yScale_h(d.humidity); });

        d3.selectAll("g").remove();

        line_chart = d3.select("#line_chart")
              .attr("width", w + margin.left + margin.right)
              .attr("height", h + margin.top + margin.bottom/10)
              .attr('preserveAspectRatio', 'xMidYMid meet')
              .attr('viewBox', '0 0 ' + (w+margin.left+margin.right) + ' ' + (h+margin.top+margin.bottom))
            .append("g")
              .attr("transform", "translate(" + margin.left + "," + (margin.top+75) + ")");

        // Draw lines
        line_chart.append("path")
            .datum(dataset)
            .attr("class", "line_temp")
            .attr("d", line_t);

        line_chart.append("path")
            .datum(dataset)
            .attr("class", "line_humid")
            .attr("d", line_h);

        // Add axes
        function add_axis_hour(svg) {
          svg.append("g")
                .attr("class", "axis_hour")
                .attr("transform", "translate(0," + h + ")")
                .call(xAxis_hour)
              .selectAll("text")
                .attr("y", 0)
                .attr("x", 10)
                .attr("dy", ".35em")
                .attr("transform", "rotate(90)")
                .style("text-anchor", "start");
        }

        function add_axis_day(svg) {
          svg.append("g")
                .attr("class", "axis_day")
                .attr("transform", "translate(0," + (h+50) + ")")
                .call(xAxis_day)
              .selectAll("text")
                .attr("y", 0)
                .attr("x", 10)
                .attr("dy", "1.25em")
                .style("text-anchor", "start");
        }

        function add_axis_left(svg, axisToAdd, axisLabel, chartTitle) {

          svg.append("g")
                .attr("class", "axis_left")
                .call(axisToAdd);

          svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x",0 - (h / 2))
                .attr("dy", ".75em")
                .style("text-anchor", "middle")
                .attr("class", "axis_left_label")
                .text(axisLabel);

          svg.append("text")
                .attr("class", "chart_title")
                .attr("x", -10)
                .attr("y", -15)
                .attr("text-anchor", "start")
                .text(chartTitle);
        }

        function add_axis_right(svg, axisToAdd, axisLabel) {
          svg.append("g")
                .attr("class", "axis_right")
                .attr("transform", "translate(" + w + ", 0)")
                .call(axisToAdd);

          svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", w + (margin.right/1.25))
                .attr("x",0 - (h / 2))
                .attr("dy", ".75em")
                .style("text-anchor", "middle")
                .attr("class", "axis_right_label")
                .text(axisLabel);
        }

        // add_axis_hour(line_chart);
        // add_axis_day(line_chart);
        line_chart.append("line")
              .attr("class", "h_line")
              .attr("y1", h)
              .attr("y2", h)
              .attr("x1", 0)
              .attr("x2", w);

        add_axis_left(line_chart, yAxis_left, "Temperature (F)", "Temperature and Humidity");
        add_axis_right(line_chart, yAxis_right, "Humidity (%)");

        // Add tooltip
        var focus = line_chart.append("g")
              .style("display", "none")
              .attr("class", "t");

        // Circles for each line
        focus.append("circle")
              .attr("class", "t")
              .style("fill", "cornflowerblue")
              .style("stroke", "cornflowerblue")
              .attr("r", 4);

        focus.append("circle")
              .attr("class", "h")
              .style("fill", "salmon")
              .style("stroke", "salmon")
              .attr("r", 4);

        // Text for the date and each line
        focus.append("text")
              .attr("class", "d");

        focus.append("text")
              .attr("class", "t");

        focus.append("text")
              .attr("class", "h");

        focus.append("line")
              .attr("class", "v_line")
              .attr("y1", 0)
              .attr("y2", (h));

        function draw_tooltip_1(date_t, temp, date_h, humidity) {
              focus.select("circle.t")
                  .transition()
                  .duration(75)
                  .attr("transform",
                        "translate(" + xScale_t(date_t) + "," +
                                       yScale_t(temp) + ")");

              focus.select("circle.h")
                  .transition()
                  .duration(75)
                  .attr("transform",
                        "translate(" + xScale_h(date_h) + "," +
                                       yScale_h(humidity) + ")");

              focus.select("line.v_line")
                  .transition()
                  .duration(75)
                  .attr("x1", xScale_t(date_t))
                  .attr("x2", xScale_t(date_t));

              focus.select("text.d")
                  .transition()
                  .duration(75)
                  .text(formatTime(date_t))
                  .attr("transform",
                        "translate(" + xScale_t(date_t) + "," +
                                       (margin.top*.2) + ")");

              focus.select("text.t")
                  .transition()
                  .duration(75)
                  .text("Temperature: " + temp + "F")
                  .attr("transform",
                        "translate(" + xScale_t(date_t) + "," +
                                       (margin.top*.6) + ")");

              focus.select("text.h")
                  .transition()
                  .duration(75)
                  .text("Humidity: " + humidity + "%")
                  .attr("transform",
                        "translate(" + xScale_t(date_t) + "," +
                                       (margin.top) + ")");
        }

        // SVG to detect mouse movements
        line_chart.append("rect")
              .attr("width", w)
              .attr("height", h)
              .style("fill", "none")
              .style("pointer-events", "all")
              .on("mouseover", mouse_over)
              .on("mouseout", mouse_out)
              .on("mousemove", mousemove);

// --------------------------------------------------------------------------//
// WIND COMPASS
// --------------------------------------------------------------------------//
        var wind_w = 250,
            wind_h = 250,
            padding = {top: 30, right: 10, bottom: 10, left: 10};

        // Create SVG
        var wind_compass = d3.select("#wind_compass")
            .attr("width", wind_w)
            .attr("height", wind_h)
            .attr("class", "wind_compass_svg")
            .attr('preserveAspectRatio', 'xMidYMin meet')
            .attr('viewBox', '0 -20 ' + (wind_w+padding.left+padding.right) + ' ' + (wind_h+padding.top+padding.bottom))

        var radius = Math.min(wind_w, wind_h / 2);

        var arcScale = d3.scaleLinear()
                  .domain([min_ws, max_ws])
                  .range([0, wind_w/2]);

        // Draw compass circles
        circle_radii = [1.25, 2.5]
        wind_compass.selectAll("circle")
              .data(circle_radii)
              .enter()
              .append("circle")
              .attr("cx", wind_w/2)
              .attr("cy", wind_h/2)
              .style("stroke", "grey")
              .style("fill", "rgba(255, 255, 255, 0)")
              .attr("r", function(d) { return radius/d; })
              .attr('preserveAspectRatio', 'xMidYMin meet')
              .attr('viewBox', '0 0 ' + wind_w + ' ' + wind_h);

        // Add text for cardinal directions
        cardinal = [{ 'direction': 'N', 'loc': [wind_w/2, padding.top-30] },
                    { 'direction': 'W', 'loc': [padding.left, wind_h/2] },
                    { 'direction': 'S', 'loc': [wind_w/2, wind_h-padding.bottom] },
                    { 'direction': 'E', 'loc': [wind_w-padding.right, wind_h/2] }]

        wind_compass.selectAll("text")
              .data(cardinal)
              .enter()
              .append("text")
              .attr("transform", function(d) {
                return "translate(" + d.loc[0] + "," + d.loc[1] + ")";
              })
              .attr("class", "compass_label")
              .attr("text-anchor", "middle")
              .text(function(d) { return d.direction} );

        wind_compass.append("text")
              .attr("class", "compass_title")
              .attr("x", -25)
              .attr("y", margin.top/2)
              .attr("text-anchor", "start")
              .text("Wind Direction");

        wind_compass.append("text")
              .attr("class", "compass_title")
              .attr("x", -25)
              .attr("y", margin.top+5)
              .attr("text-anchor", "start")
              .text("and Speed");

        // Create arc container
        var needle = wind_compass.selectAll("arc")
            .data(dataset)
            .enter()
            .append("g")
            .attr("class", "arc")
            .attr("transform", "translate(" + (wind_w/2) + "," + (wind_h/2) + ")");

        needle.append("path")
            .attr("class", "arc");

        needle.append("text")
            .attr("dy", ".35em")
            .style("text-anchor", "middle")
            .attr("class", "wedge_label")

        // Function to draw the arc which is called on mouseover
        var wspd = 0,
            dir = 0;
        function draw_arc(wspd, dir) {
              var startAng,
                  endAng;

              if (dir >=0 & dir <= 5) {
                startAng = 355
                endAng = 365
              } else {
                startAng = +dir-5
                endAng = +dir+5
              }

              function arcTween(b) {
                  var i = d3.interpolate({value: b.previous}, b);
                  return function(t) {
                      return arc_wind(i(t));
              };
            }
              // Create arc generator with placeholders
              var arc_wind = d3.arc()
                  .innerRadius(0)
                  .outerRadius(arcScale(wspd))
                  .startAngle(startAng*(Math.PI/180))
                  .endAngle(endAng*(Math.PI/180));

              // Draw the arc and text
              needle.select("path.arc")
                  .transition()
                  .duration(200)
                  .attr("d", arc_wind())
                  .attrTween("d", arcTween);

              // Add wind text
              needle.select("text.wedge_label")
                    .attr("transform", "translate(0, 0)")
                    .transition()
                    .duration(75)
                    .text(function(d) {
                      var msg = (dir + "\u00B0 at " + wspd + "mph");
                      return msg;
                      });

        } // end of draw_arc()

    // -----------------------------------------------------------------------//
    // CLOUD AND PRECIPITATION CHART
    // -----------------------------------------------------------------------//
            // Additional scale function
            var yScale_c = d3.scaleLinear()
                     .domain([
                      parseInt(d3.min(dataset, function(d) { return d.cloudCover; }))*.90,
                      parseInt(d3.max(dataset, function(d) { return d.cloudCover; }))*1.1
                    ])
                     .range([h, 0]);

            // SVG object of chart
            var area_chart = d3.select("#area_chart")
                  .attr("width", w + margin.left + margin.right)
                  .attr("height", h + margin.top + margin.bottom/10)
                  .attr('preserveAspectRatio', 'xMidYMin meet')
                  .attr('viewBox', '0 0 ' + (w+margin.left+margin.right) + ' ' + (h+margin.top+margin.bottom))
                .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            // Axes
            var yAxis_left_cc = d3.axisLeft()
                  .scale(yScale_h)
                  .tickSize(0)
                  .ticks(10);

            var yAxis_right_pp = d3.axisRight()
                  .scale(yScale_h)
                  .tickSize(0)
                  .ticks(10);

            add_axis_hour(area_chart);
            add_axis_day(area_chart);
            add_axis_left(area_chart, yAxis_left_cc, "Cloud Cover (%)", "Cloud Cover and Chance of Precipitation");
            add_axis_right(area_chart, yAxis_right_pp, "Probability of Precipitation (%)");

            // Area for cloud cover
            var area_c = d3.area()
                  .x(function(d) { return xScale_t(d.date_cc); })
                  .y0(function() { return yScale_h.range()[0]; })
                  .y1(function(d) { return yScale_h(d.cloudCover); });

            area_chart.append("path")
                .datum(dataset)
                .attr("class", "area_cloud")
                .attr("d", area_c);

            // Line for probablity of precipitation
            var line_pp = d3.line()
                  .x(function(d) { return xScale_t(d.date_t); })
                  .y(function(d) { return yScale_h(d.precipProb); })
                  .curve(d3.curveStepAfter);

            area_chart.append("path")
                  .datum(dataset)
                  .attr("class", "line_pp")
                  .attr("d", line_pp);

            // Add tooltip elements
            var focus_2 = area_chart.append("g")
                  .attr("class", "cc");

            focus_2.append("circle")
                  .attr("class", "cc")
                  .style("fill", "rgba(100, 149, 237, 1.0)")
                  .style("stroke", "rgba(100, 149, 237, 1.0)")
                  .style("display", "none")
                  .attr("r", 4);

            focus_2.append("text")
                  .attr("class", "cc");

            focus_2.append("text")
                  .attr("class", "pp");

            focus_2.append("line")
                  .attr("class", "v_line_2")
                  .attr("y1", 0)
                  .attr("y2", (h));

            // Function to draw second tooltip
            function draw_tooltip_2(date_cc, cloudCover, date_t, precipProb) {
                  focus_2.select("circle.cc")
                      .transition()
                      .duration(75)
                      .attr("transform",
                            "translate(" + xScale_h(date_cc) + "," +
                                           yScale_h(cloudCover) + ")");

                  focus_2.select("line.v_line_2")
                      .transition()
                      .duration(75)
                      .attr("x1", xScale_t(date_t))
                      .attr("x2", xScale_t(date_t));

                  focus_2.select("text.cc")
                      .transition()
                      .duration(75)
                      .text("Cloud Cover: " + cloudCover + "%")
                      .attr("transform",
                            "translate(" + xScale_t(date_t) + "," +
                                           (margin.top*.2) + ")");

                  focus_2.select("text.pp")
                      .transition()
                      .duration(75)
                      .text("Probability of Precipitation: " + precipProb + "%")
                      .style("display", function(d) {
                        if (precipProb == null) {
                          return "none";
                        } else {
                          {
                            return "inline";
                          }
                        }
                      })
                      .attr("transform",
                            "translate(" + xScale_t(date_t) + "," +
                                           (margin.top*.6) + ")");
            } // end of function for second tool tip

            // SVG to detect mouse movements
            area_chart.append("rect")
                  .attr("width", w)
                  .attr("height", h)
                  .style("fill", "none")
                  .style("pointer-events", "all")
                  .on("mouseover", mouse_over)
                  .on("mouseout", mouse_out)
                  .on("mousemove", mousemove);
// --------------------------------------------------------------------------//
// ---------- Function to return values on mousemove ---------- //
// --------------------------------------------------------------------------//
        function mousemove() {
            var x0 = xScale_t.invert(d3.mouse(this)[0]),
                i = bisectDate(dataset, x0, 1),
                d0 = dataset[i - 1],
                d1 = dataset[i],
                d = x0 - d0.date_t > d1.date_t - x0 ? d1 : d0;


            draw_tooltip_1(d.date_t, d.temp, d.date_h, d.humidity);
            draw_arc(d.wind_speed, d.direction);
            draw_tooltip_2(d.date_cc, d.cloudCover, d.date_t, d.precipProb);
        } // end of mousemove function

        function mouse_over() {

          focus.style("display", null);

          needle.select("path.arc")
              .style("display", null);

          focus_2.select("text.cc")
              .style("display", null);

          focus_2.select("text.pp")
              .style("display", null);

          focus_2.select("circle.cc")
              .style("display", null);

          focus_2.select("line.v_line_2")
              .style("display", null);
        }

        function mouse_out() {
          focus.style("display", "none");

          needle.select("path.arc")
              .style("display", "none");

          focus_2.select("text.cc")
              .style("display", "none");

          focus_2.select("text.pp")
              .style("display", "none");

          focus_2.select("circle.cc")
              .style("display", "none");

          focus_2.select("line.v_line_2")
              .style("display", "none");
        }

  // }); // end of json load
}
