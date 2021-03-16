/******************************************************************************************
 * Get every index in every dimension
 * @extends {Array}                               Used array   
 * @param  {function(val,brunch,index)} callBack  Callback to execute for every index found
 *-----------------------------------------------
 * @example [[[0,1,2],1],4].onIndexCall(function(x1,x2,x3){console.log(x1)});
 */
Array.prototype.onIndexCall = function(callBack = function(x){}){
    var guide = [0];
    var result = [];
            var chunk = this;
            for(;guide.length>0;){
                var obj = chunk[guide[guide.length-1]];
                /** Go deeper **/
                if(obj!==undefined && Array.isArray(obj)){
                    chunk = obj;
                    guide.push(0);
                /** Move throught (add 1 to index) **/
                }else if(obj!==undefined){
                    callBack(obj,guide.length,guide[guide.length-1]);
                    guide[guide.length-1] +=1;
                /** Get back (delete last index + add 1 to main index + get new array ot chunk) **/
                }else{
                    guide.pop();                    //delete last index
                    guide[guide.length-1] += 1;     //increase the last dimension
                    var chunk = this;               
                    guide.map((p,i)=>{              //get array of that dimension
                        Array.isArray(chunk[p])?
                        chunk = chunk[p]:false;});
                }
             }
}

/***************************************************************
//Example usage:
/***************************************************************/
var a = [[1,2,[[[[3,4,5]]]],6],7,8];
a.onIndexCall(function(x,x1,x2){console.log(`Value:${x}; Branch Nº:${x1}; Branch index:${x2}`)});
