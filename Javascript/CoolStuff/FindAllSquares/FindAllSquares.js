//*****************************************
//    CREATED BY: Ricardo Ribeiro
//    Big thanks to: Andre Dos Santos
//*****************************************
//    Notes: It works only when nLine != nColumns
//    and for not null points
//*****************************************

//Matrix scheme 
// (matrix[0] = line zero) (matrix[0][1] = column one of the line zero)
const matrix = [
[1,1,1,1],
[1,1,1,1],
[1,1,1,1],
];


//number of rows on the matrix
const mRows = matrix.length;   

//number of columns on the matrix
const mColumns = matrix[0].length;  

//Calculate the number of points
const points = mRows * mColumns;

//All horizontal and vertical lines. Like: 1 square = 4 lines
const lines = ((mRows - 1) * mColumns) + ((mColumns - 1) * mRows)

//Find the iterator and stablish only positive values: |i|
let i = mColumns - mRows;
i = i < 0 ? i * -1 : i;

//Find small squares
const qP = (mRows - 1) * (mColumns - 1);

//Find big squares
const qG = (lines - points - i - qP) * -1;

console.log('Small Squares: ' + qP + 
         ';  Big Squares:' + qG +
         ';  Total:' + (qP + qG));
