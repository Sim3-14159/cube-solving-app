# cube-solving-app 

### This repository contains my 3x3 Rubik's Cube solver app GUI.
---

## Files
- The directory `Rubik'sCubeSolver` contains the main Python file, `Rubik'sCubeSolver.py`, and all of the files it is dependent on to run:
  - You can find the main Python file in [`Rubik'sCubeSolver/Rubik'sCubeSolver.py`](Rubik'sCubeSolver/Rubik'sCubeSolver.py).
  - The file [`Rubik'sCubeSolver/Rubik'sCubeSolverMode.txt`](Rubik'sCubeSolver/Rubik'sCubeSolverMode.txt) contains the the mode of the GUI, *light*, *dark*, or *auto*.

- The directory [`Executables`](Executables) contains a shortcut to the script and it's dependencies, which are located in [`Executables/.Rubik'sCubeSolver`](Executables/.Rubik'sCubeSolver). To run, you need place the contents of `Executables` in your desktop. Here is how to do that on a Raspberry Pi:
  ```bash
  cd # whatever/directory/you/put/your/GitHub/projects
  ```
  ```bash
  git clone "https://github.com/Sim3-14159/cube-solving-app.git"
  ```
  ```bash
  cp -r ./cube-solving-app/Executables/* ~/Desktop/ 
  ```
  You should now have a file called *Rubik'sCubeSolver* that you can double click to open my app!

--- 
## Dependencies 

> [!NOTE]
> You do not need any of these if you are running the directly executable file.
<br>


| Modules |
|--------------|
| tkinter *v8.5+* |
| kociemba *v1.2.1+* |

<br>

| Language | Version |
|--|--|
| Python | 3.*x*
