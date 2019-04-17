# ApplyScaleAndResizeModifiers2.8
Applies selected object's scale and resizes modifiers to stay consistent with the new scale.

## Features  
Supported Modifiers
* Array  
  * Resizes constant offset
* Bevel
* Solidify
* Wireframe
* Cast
* Displace  
  * Resizes strength
  * If using Global, Local, or Object coordinates with a procedural noise, resizes the assigned texture  
* Hook
* Wave

## Installation  
### Requirements  
Works on Windows, Mac, and Linux.  
Meant for Blender 2.8 Beta
### How to Install  
Download the python file (put it in a place where you can easily find it, like your desktop)  
In Blender's settings, go to the addons tab  
At the bottom, click "Install from File"  
Find where you put the python file, select it, and click "Install from File" 

## Using
1. Run the operator from...
* Operator Search > Apply Scale and Resize Modifiers  
2. The operator will resize the selected objects' modifiers and apply scale.
3. Change Resize Source to get a possibly better result if the object's scale is not uniform.

## Notes
Works best with objects that have uniform scale. If scale isn't uniform, use Resize Source to get a possibly better result.
