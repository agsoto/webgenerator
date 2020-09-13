window.annotations = [];

$(document).ready(function() {

    function annotate(element) {
      var position = element.offset();
      var width = element.innerWidth();
      var height = element.innerHeight();

      var rect = {
        name: "rect",
        x: parseInt(position.left),
        y: parseInt(position.top),
        width: parseInt(width),
        height: parseInt(height)
      };

      var region = {
        "shape_attributes": rect,
        "region_attributes": {
            "type": $(element).data("wg-type")
        }
      }

      //Only for debugging - draw bounding box
      // $('<div/>',{
      //     'css' : {
      //         'content': ' ',
      //         'position': 'absolute',
      //         'left' : rect.x,
      //         'width' : width, 
      //         'top' : rect.y, 
      //         'height' : height,
      //         'border' : '3px solid black'
      //     }
      // }).appendTo('body');
      return region;
    }

    //getBoundingBox(ele);
    //positionsString = $('#BoundingBoxesValues');
    var screenshotHeight = window.screenshotHeight;

    if(typeof screenshotHeight === 'undefined'){ //Simplify screenshot height logic, not set means fullscreen
      screenshotHeight = window.innerHeight;
    }

    $('[data-wg-type]').each(function(i,ele) { 
        if($(ele).offset().top < screenshotHeight){
          let newAnnotation = annotate($(ele));
          if((newAnnotation.shape_attributes.y+newAnnotation.shape_attributes.height) > screenshotHeight){
            newAnnotation.shape_attributes.height = screenshotHeight-newAnnotation.shape_attributes.y;
          }
          window.annotations.push(newAnnotation);
        }
        //getBoundingBox($(ele));
    });
    
    //positionsString.val(JSON.stringify(boxes)); This method escaped the double quotes when getting the value from selenium driver
    //console.log(getBoundingBox($('#cosito')))
  });
  