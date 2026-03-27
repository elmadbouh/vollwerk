# Vectorworks Python Scripting API Documentation Overview

Vectorworks provides an embedded Python scripting environment (Python 3) via the `vs` module. This allows you to manipulate document geometry, layers, classes, and preferences in Vectorworks programmatically. 

## 1. Importing the API
In any Vectorworks Python script, the `vs` wrapper module is imported.
```python
import vs
```

## 2. Basic Document Structure Functions
Vectorworks structures drawing into **Layers** and **Classes**.

- `vs.Layer(layerName)`: Makes the specified design layer or sheet layer active. If it doesn't exist, it creates a new layer with that name.
- `vs.GetLayerByName(layerName)`: Returns the handle to the specified layer.
- `vs.NameClass(className)`: Makes the specified class active. Creates it if it doesn't exist.
- `vs.GetLName(handle)`: Gets the name of the layer or class handle.

## 3. Object Creation and Handles
Every object (line, polygon, symbol, wall, etc.) is referenced by a Handle (a unique internal ID object). Handle variables are often named `h`.
- `vs.LActLayer()`: Returns a handle to the last object exactly matching on the active layer.
- `vs.FInLayer(layerHandle)`: Gets the first object in the specified layer list.
- `vs.NextObj(handle)`: Gets the next object after the given handle.

## 4. Traversing Objects
You typically traverse all objects on a layer using a While loop.
```python
layer_h = vs.GetLayerByName('MyLayer')
obj_h = vs.FInLayer(layer_h)
while obj_h != None:
    # Do something with obj_h
    obj_h = vs.NextObj(obj_h)
```
Alternatively, you can use `vs.ForEachObject(callback, criteria)` which is much more efficient.
```python
def process_obj(h):
    # modify object
    pass

vs.ForEachObject(process_obj, "((L='MyLayer'))")
```

## 5. Modifying Object Properties
When transforming drawings from Draft ("Vorentwurf") to Application ("Antrag"), you frequently need to change line weights, colors, or transfer objects to new layers/classes.

- `vs.SetClass(handle, className)`: Changes the object's class.
- `vs.SetLW(handle, lineWeight)`: Changes line weight in Mils.
- `vs.SetFPat(handle, pattern)`: Set fill pattern (backcolor, forecolor, etc.)
- `vs.SetPenColorByClass(handle)` / `vs.SetFillColorByClass(handle)`: Forces the object to take properties from its class.
- `vs.SetLayer(handle, layerHandle)`: Moves the object to another layer.

## 6. Duplicating Objects
- `vs.CreateDuplicateObject(handle, targetHandle)`: Duplicates an object.

## Reference Limits
The complete Vectorworks Developer documentation is hosted at:
[developer.vectorworks.net](https://developer.vectorworks.net/index.php/Python)

For further scripting, you usually lookup `VS:Function Reference` online. As it's locked behind anti-scraping checks on developer.vectorworks.net, this document holds the main primitives required for batch-processing and transforming layers.
