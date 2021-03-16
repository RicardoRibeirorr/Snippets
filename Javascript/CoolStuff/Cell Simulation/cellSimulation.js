/************************************
         **   @Title  Single Cell Simulation
         **   @Author Ricardo O'Ribeiro
         *************************************
         **   @Use Copy and past code to
         **        P5.js website editor
         *************************************/

        /************************************
         **   Options
         *************************************/
        let asWalls = false; //true = add walls




        /************************************
         **   Variables
         *************************************/
        let cols = 60;
        let rows = 60;
        let cellGridSize = 10;
        let squareSize = 6;
        let grid = [];
        let nextGrid = [];



        /************************************
         **   Functions
         *************************************/
        function create2D(n_cols, n_rows) {
            var ar = Array(n_rows);
            for (var i = 0; i < n_rows; i++)
                ar[i] = Array(n_cols);
            return ar;
        }

        function setup() {
            nextGrid = create2D(cols, rows);
            grid = create2D(cols, rows);
            //set random values for the grids
            for (var x = 0; x < rows; x++) {
                for (var y = 0; y < cols; y++) {
                    if (x < cellGridSize && y < cellGridSize) {
                        var r = floor(random(2));
                        if (y == 0 || x == 0 || y == cellGridSize - 1 || x == cellGridSize - 1)
                            grid[x][y] = 0;
                        else
                            grid[x][y] = r;
                    } else {
                        //create walls
                        var rand = random(2);;
                        if (rand < 0.15 && asWalls === true) {
                            grid[x][y] = -100;

                        } else
                            grid[x][y] = 0
                    }
                    nextGrid[x][y] = 0;
                }
            }
            createCanvas(600, 600);
        }

        function draw() {
            background(220);
            rulesCheck();
            for (var x = 0; x < rows; x++) {
                for (var y = 0; y < cols; y++) {
                    drawGrid(x, y);
                }
            }

            let temp = grid;
            grid = nextGrid;
        }

        function drawGrid(x, y) {
            //fill the squeares
            if (grid[x][y] == 1) fill(0, 0, 0);
            else if (grid[x][y] > 1) {
                fill(0, 20, 0);
                grid[x][y] = 1
            } else if (grid[x][y] == -1) {
                fill(20, 0, 0);
                grid[x][y] = 0
            } else if (grid[x][y] == -100) {
                fill(0, 0, 255);
            } else fill(255);
            stroke(0);
            rect(x * squareSize, y * squareSize, squareSize - 1, squareSize - 1);
        }


        function rulesCheck() {
            for (var x = 0; x < rows; x++) {
                for (var y = 0; y < cols; y++) {
                    var n_nayboars = 0;
                    //check nayboars vertical & horizontal
                    for (let i = -1; i <= 1; i++) {
                        for (let j = -1; j <= 1; j++) {
                            if (x > 0 && x < rows - 1 && y > 0 && y < cols - 1)
                                if (grid[x + i][y + j] !== -100)
                                    n_nayboars += grid[x + i][y + j] > 0 ? 1 : 0;
                        }
                    }
                    n_nayboars -= grid[x][y];

                    //rules  
                    if (n_nayboars < 2 && grid[x][y] == 1) nextGrid[x][y] = -1; //die
                    if (n_nayboars > 3 && grid[x][y] == 1) nextGrid[x][y] = -1; //die
                    if (n_nayboars === 3 & grid[x][y] !== 1) nextGrid[x][y] = 2; // live
                    else nextGrid[x][y] = grid[x][y];
                }
            }
        }

        // reset board when mouse is pressed
        function mousePressed() {
            setup();
        }


        function toggleWalls() {
            asWalls = !asWalls;
            setup();
        }

        function submitGridChanges(){
            cols = document.getElementById("gridCols").value;
            rows = document.getElementById("gridRows").value;
            setup();
        }

        function submitSquareChanges(){
            squareSize = document.getElementById("squareSize").value;
            setup();
        }


        function submitCellChanges(){
            cellGridSize = document.getElementById("cellGridSize").value;
            setup();
        }
