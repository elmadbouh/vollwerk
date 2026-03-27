import vs

# --- Configuration Section ---

# The original Draft (Vorentwurf) Layer. Mentioned as Level 9.
SOURCE_LAYER = 'GR-OG-4'

# The expected Target (Antrag) Layer. Mentioned as Level 11.
TARGET_LAYER = 'GR-OG'

# Class Mapping Table:
# Maps sketchy/draft classes to formal application/permit classes.
# The exact class names will depend on your specific standard, these are placeholders.
CLASS_MAPPING = {
    'AR-Wand-Vorentwurf': 'AR-Wand-Massiv',
    'AR-Fenster-Skizze': 'AR-Fenster-Detail',
    'AR-Moebel-Vorab': 'AR-Moebel',
    # Add further draft-to-final class mappings relevant to 1513_E_GR_v2016_v2026.vwx here.
}

def setup_target_layer():
    """
    Ensure the target layer exists and is configured.
    Moves execution to the target layer.
    """
    # Create or switch to TARGET_LAYER
    vs.Layer(TARGET_LAYER)  
    h_target_layer = vs.GetLayerByName(TARGET_LAYER)
    
    if h_target_layer != None:
        # Optionally, apply elevation / level properties depending on how 'Level 11' is defined.
        # Let's assume the user already has this layer set to Level 11 in their document's story options,
        # or we just rely on standard layer switching.
        pass
        
    return h_target_layer

def standardize_object_styles(h_obj):
    """
    Callback function that standardizes objects to match the formal 'Antrag' 
    visual representation constraints, removing 'Vorentwurf' stylisation.
    """
    # 1. Map classes
    obj_class = vs.GetClass(h_obj)
    if obj_class in CLASS_MAPPING:
        # Update class reference to strict mapping
        vs.SetClass(h_obj, CLASS_MAPPING[obj_class])
        
    # 2. Force Properties 'ByClass'
    # Draft documents often have manual styling overrides (colors, line thicknesses).
    # 'Antrag' documents typically require standardizing them by strictly adhering to Class attributes.
    vs.SetFPatByClass(h_obj)     # Fill pattern by class
    vs.SetLSByClass(h_obj)       # Line style by class
    vs.SetLWByClass(h_obj)       # Line weight by class
    vs.SetPenColorByClass(h_obj) # Pen color by class
    vs.SetFillColorByClass(h_obj)# Fill color by class

    # 3. Strip Sketch Styles
    # Ensures that if "sketch rendering" was applied to the objects, it is stripped.
    # We set the sketch style drop-down variable to 0. (ObjectVariable 169 holds Sketch Style).
    # We only apply this to specific object types that support sketch styles to prevent constant 169 errors.
    # Supported types: Lines(2), Rects(3), Ovals(4), Polys(5), Arcs(6), Polylines(21), Walls(68)
    obj_type = vs.GetTypeN(h_obj)
    if obj_type in [2, 3, 4, 5, 6, 21, 68]:
        try:
            vs.SetObjectVariableInt(h_obj, 169, 0)
        except Exception:
            pass

def execute_layer_transformation():
    """
    Iterates over the source layer, duplicates the contents onto the target layer, 
    and applies standardizations to visually match the final PDF.
    """
    vs.Message("Initializing Draft 'Vorentwurf' to Final 'Antrag' Transfer...")
    
    # 1. Try to get a handle for the Source Layer
    h_source = vs.GetLayerByName(SOURCE_LAYER)
    if h_source == None:
        vs.AlrtDialog(f"Error: Could not locate source layer: '{SOURCE_LAYER}'. Please verify the layer name.")
        return
        
    # 2. Prepare the Target Layer
    h_target = setup_target_layer()
        
    # 3. Traverse through objects on the source layer
    h_obj = vs.FInLayer(h_source)
    duplicate_count = 0
    
    while h_obj != None:
        # Duplicate the object directly onto the target layer
        h_dup = vs.CreateDuplicateObject(h_obj, h_target)
        
        # 4. Standardize the newly duplicated target object
        if h_dup != None:
            standardize_object_styles(h_dup)
            duplicate_count += 1
            
        # Move on to the next object in the source layer
        h_obj = vs.NextObj(h_obj)
        
    # 5. Re-focus camera and UI on Target Layer, then redraw all to apply changes
    vs.Layer(TARGET_LAYER)
    vs.RedrawAll()
    
    # Complete
    vs.AlrtDialog(
        f"Layer Transformation Successful!\n\n"
        f"Copied {duplicate_count} objects from {SOURCE_LAYER} to {TARGET_LAYER}.\n"
        f"Class mappings, strict 'ByClass' overrides, and style removals were applied to match the final Antrag appearance."
    )

# Run the transformation
execute_layer_transformation()
