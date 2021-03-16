
//***************************************
//  SET BASIC DATA -> (x,y)
var x = [17,13,12,15,16,14,16,16,18,19];
var y = [94,73,59,80,93,85,66,79,77,91];
var toPredictX = 15; //the (x) value to predict with
var predictedY = 0; //the prediction result (y) for given (x)
//***************************************
// CALCULATE THE MEAN FOR EACH DATA TYPE -> (x^, y^)
var xMean = x.reduce((acc,v) => acc + v) / x.length;
var yMean = y.reduce((acc,v) => acc + v) / y.length;
//***************************************
// CALCULATE THE STRENGHT OF THE RELATIONSHIP -> (r)
// (x-x^)*(y-y^) / sqrt(pow(x-x^) * pow(y-y^))
var r = CorrelationCoefficient();
//***************************************
// Standard DEVIASION ERROR -> (sX, sY)
// sX = sqrt(pow(x-x^) / n-1); sY = sqrt(pow(y-y^) / n-1);  
var [sX,sY] = StandardDeviation(); 
//***************************************
// SLOPE BASED OF THE STANDARD DEVIATION -> (b) or (m)
var b = r * (sY/sX); // b = r * (sY/sX)
//***************************************
// INTERCEPTION OF y VALUES -> (a) or (c)
var a = yMean - b*xMean; // a = y^ - b*x^
//***************************************



//***************************************
// LINEAR REGRESSION PREDICTION
predictedY = a + b*toPredictX; // y = a+b*x
//***************************************



//***********FUNCTION***************
// CALCULATE THE (r) STRENGHT OF THE 
// RELATIONSHIP BETWEEN VARIABLES x & y
function CorrelationCoefficient(){
  var minLenght  = x.length<y.length?x.length:y.length;
  var top = x_xMean2 = y_yMean2 = 0;
  
	for(var i=0; i<minLenght ; i++){
  	var x_xMean = x[i] - xMean; // (x-x^)
    var y_yMean = y[i] - yMean; // (y-y^)
    top += (x_xMean*y_yMean); // (x-x^)*(y-y^)
    x_xMean2 += Math.pow(x_xMean,2); //(x-x^)^2
    y_yMean2 += Math.pow(y_yMean,2); //(y-y^)^2
  }

  // (x-x^)*(y-y^) / sqrt(pow(x-x^) * pow(y-y^))
  return top / Math.sqrt((x_xMean2*y_yMean2));
}
//***************************************



//************FUNCTION*********************
// STANDAD DEVIATION
function StandardDeviation(){
  var minLenght  = x.length<y.length?x.length:y.length;
  var x_xMean2 = 0;
  var y_yMean2 = 0;
  
	for(var i=0; i<minLenght ; i++){
  	var x_xMean = x[i] - xMean; // (x-x^)
    var y_yMean = y[i] - yMean; // (y-y^)
    x_xMean2 += Math.pow(x_xMean,2); //pow(x-x^)
    y_yMean2 += Math.pow(y_yMean,2); //pow(y-y^)
  }
  
  return [Math.sqrt(x_xMean2/(minLenght-1)), // sqrt(pow(y-y^) / n-1)
  			  Math.sqrt(y_yMean2/(minLenght-1))];// sqrt(pow(x-x^) / n-1)
}
//***************************************




//**********PLOT*******************
// IGNORE IF YOU WISH
//**********PLOT*******************
  // PLOT VALUES
var originData = {x:x,y:y};
var predictionPoint = {x:[toPredictX],y:[predictedY]};
  //Create the line that passes through
var predictLine = {x:[11,20],y:[a + b*11, a + b*20]} // y = a + b*x
plot(originData, predictionPoint, predictLine);
//***************************************











