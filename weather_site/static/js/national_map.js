
var margin = {top: 50, right: 50, bottom: 50, left: 50},
    w = 900 - margin.left - margin.right,
    h = 600 - margin.top - margin.bottom;

// Use the extracted size to set the size of an SVG element.
national_map = d3.select("#national_map")
      .attr("width", w)
      .attr("height", h)
      .attr('preserveAspectRatio', 'xMidYMin')
      .attr('viewBox', '0 0 ' + w + ' ' + h);

//Define map projection and path generator
var projection = d3.geoAlbersUsa();
var path = d3.geoPath()
       .projection(projection);

//Load in GeoJSON data
d3.json("static/us-states.json", function(json) {

  //Bind data and create one path per GeoJSON feature
  national_map.selectAll("path")
     .data(json.features)
     .enter()
     .append("path")
     .attr("d", path)
     .style("fill", "cornflowerblue")
     .style("stroke", "white")
     .style("stroke-width", 1);

     d3.json("static/us-cities.json", function(data) {

       data.forEach(function(d) {
          d.coords.long = +d.coords.long,
          d.coords.lat = +d.coords.lat
        });

        data = data.filter(function(d) {
              return projection([+d.coords.long, +d.coords.lat]) != null
        })

       national_map.selectAll("circle")
          .data(data)
          .enter()
          .append("circle")
          .attr("cx", function(d) { return projection([+d.coords.long, +d.coords.lat])[0]; })
          .attr("cy", function(d) { return projection([+d.coords.long, +d.coords.lat])[1]; })
          .attr("r", 3)
          .style("fill", "red")
          .on("mouseover", function(d) {
            var x = projection([+d.coords.long, +d.coords.lat])[0],
                y = projection([+d.coords.long, +d.coords.lat])[1],
                city = d.city;

            showCity(x, y, city);
          })
          .on("mouseout", hideCity);

          national_map.append("text")
              .attr("class", "cityText");

          function showCity(x, y, city) {
                national_map.select("circle")
                    .attr("r", 10)
                    .attr("cx", x)
                    .attr("cy", y)
                    .attr("fill-opacity", 0.5)
                    .style("display", null);

                national_map.select("text.cityText")
                    .attr("x", x+20)
                    .attr("y", y+5)
                    .text(city)
                    .style("display", null);
          }

          function hideCity() {
                national_map.select("text.cityText")
                    .style("display", "none");

                national_map.select("circle").remove();
          }


     }) // end of cities data load



}); // end of loading state outline data
