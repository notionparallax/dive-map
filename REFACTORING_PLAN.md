# Dive Map Project - Improvement Analysis & Refactoring Plan

## Current Issues Identified

### 1. **Monolithic Notebook Structure**

- **Problem**: Single 40+ cell notebook doing everything
- **Impact**: Hard to navigate, debug, and maintain
- **Solution**: Split into focused notebooks (data prep, visualization, analysis, export)

### 2. **Scattered Configuration**

- **Problem**: Constants and settings spread throughout the code
- **Impact**: Hard to modify behavior, inconsistent values
- **Solution**: Centralized `config.py` with all settings

### 3. **Copy-Paste Data Loading**

- **Problem**: Repetitive depth_df creation, GPS loading patterns
- **Impact**: Bugs when updating one instance, code duplication
- **Solution**: Data loader classes with consistent interfaces

### 4. **Mixed Concerns in Functions**

- **Problem**: Functions doing both data processing AND visualization
- **Impact**: Hard to reuse, test, and modify
- **Solution**: Separate data processing from visualization

### 5. **No Type Hints or Documentation**

- **Problem**: Functions lack clear interfaces and documentation
- **Impact**: Hard to understand expected inputs/outputs
- **Solution**: Add comprehensive type hints and docstrings

### 6. **Magic Numbers and Hardcoded Values**

- **Problem**: Unexplained constants scattered throughout
- **Impact**: Hard to understand intent, modify behavior
- **Solution**: Named constants with explanatory comments

## Major Refactoring Recommendations

### A. **Modular Architecture**

```
dive-map/
├── config.py              # All configuration settings
├── data_loaders.py         # Data loading classes
├── visualization.py        # Visualization classes
├── analysis.py            # Analysis functions (contours, measurements)
├── export.py              # Export utilities (Folium, CSV)
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_main_visualization.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_export.ipynb
└── legacy/
    ├── map.ipynb          # Original (preserved)
    └── map_functions.py   # Original (preserved)
```

### B. **Data Loading Pattern**

```python
# Old way (scattered throughout notebook):
depth_df_1 = make_depth_df([...])
depth_df_2 = make_depth_df([...])
depth_df = pd.concat([depth_df_1, depth_df_2])

# New way (centralized):
processor = DiveDataProcessor()
depth_df, dives_gdf, photo_df = processor.load_all_data(
    fit_files=fit_files,
    gpx_configs=gpx_configs,
    photo_metadata=photo_meta
)
```

### C. **Configuration Management**

```python
# Old way (scattered constants):
TEXT_COLOUR = "white"
FIGURE_SIZE = (30, 18)
# ... in map.ipynb

X_OFFSET = 0.0001
# ... in map_functions.py

# New way (centralized):
from config import TEXT_COLOUR, FIGURE_SIZE, X_OFFSET
```

### D. **Visualization Classes**

```python
# Old way (monolithic plotting code):
fig, ax = plt.subplots(figsize=(30, 18))
# ... 200+ lines of plotting code

# New way (modular):
renderer = MapRenderer()
renderer.create_figure()
renderer.add_scalebar(starting_point, distances)
renderer.add_contours(contour_data, levels)
renderer.add_basemap(gdf)
renderer.finalize_plot(bounds, title)
```

## Specific Code Quality Issues

### 1. **Inconsistent Error Handling**

```python
# Current - no error handling:
with fitdecode.FitReader(file_name) as fit_file:
    # ... could fail silently

# Better:
try:
    with fitdecode.FitReader(file_name) as fit_file:
        # ...
except FileNotFoundError:
    logger.error(f"FIT file not found: {file_name}")
    return []
```

### 2. **Unclear Variable Names**

```python
# Current:
temp_df = all_df.copy(deep=True)
sparse = dives_gdf_3a.loc[...].iloc[::50, :]
v_and_p_gdf = gp.GeoDataFrame(result_rows, geometry="polygon")

# Better:
timezone_adjusted_df = all_df.copy(deep=True)
downsampled_positions = dives_gdf_3a.loc[...].iloc[::50, :]
voronoi_with_points_gdf = gp.GeoDataFrame(result_rows, geometry="polygon")
```

### 3. **Long Functions**

```python
# Current: 200+ line plotting function
# Better: Break into focused methods
def create_main_map(self):
    self._add_depth_traces()
    self._add_contours()
    self._add_markers()
    self._add_annotations()
    self._add_basemap()
```

### 4. **Inconsistent Data Processing**

```python
# Current: Manual timezone conversion in multiple places
dives_gdf.index = dives_gdf.index.tz_convert("UTC")
depth_df_1.index = depth_df_1.index.tz_convert("UTC")
photo_df.index = photo_df.index.tz_convert("UTC")

# Better: Centralized in data loaders
class DataProcessor:
    def standardize_timezones(self, *dataframes):
        # ... handle all timezone conversion consistently
```

## Performance Improvements

### 1. **Reduce Data Copying**

- Current code creates many intermediate DataFrames
- Use views and inplace operations where possible
- Consider chunked processing for large datasets

### 2. **Optimize Spatial Operations**

- Use spatial indexing for point-in-polygon operations
- Cache expensive calculations (distances, bearings)
- Consider using PostGIS for complex spatial queries

### 3. **Lazy Loading**

- Don't load all data upfront if not needed
- Implement data loading on demand
- Use generators for large datasets

## Testing Strategy

### 1. **Unit Tests**

```python
def test_fit_file_loader():
    # Test with known FIT file
    loader = FitFileLoader()
    data = loader.load_depth_data("test.fit")
    assert len(data) > 0
    assert all('dt' in record for record in data)
```

### 2. **Integration Tests**

```python
def test_full_data_pipeline():
    processor = DiveDataProcessor()
    depth_df, dives_gdf, photo_df = processor.load_all_data(...)
    # Verify data consistency across sources
```

### 3. **Visualization Tests**

```python
def test_map_generation():
    renderer = MapRenderer()
    # Test that maps generate without errors
    # Test that output files are created
```

## Migration Path

### Phase 1: Foundation (Week 1)

1. Create `config.py` with all constants
2. Create basic data loader classes
3. Test data loaders with existing data

### Phase 2: Visualization (Week 2)

1. Create visualization classes
2. Migrate plotting code to classes
3. Create demo notebook

### Phase 3: Analysis (Week 3)

1. Extract analysis functions
2. Add error handling and logging
3. Create analysis notebook

### Phase 4: Polish (Week 4)

1. Add comprehensive documentation
2. Create tests
3. Optimize performance
4. Archive old code

## Benefits of Refactoring

1. **Maintainability**: Easier to find and fix bugs
2. **Reusability**: Components can be used in different contexts
3. **Testability**: Smaller functions are easier to test
4. **Collaboration**: Clear interfaces enable team development
5. **Performance**: Optimized data loading and processing
6. **Documentation**: Self-documenting code with type hints

## Next Steps

1. **Start with config.py** - Move all constants to centralized configuration
2. **Refactor data loading** - Create the data loader classes
3. **Split the notebook** - Break into focused notebooks
4. **Add type hints** - Improve code clarity and IDE support
5. **Write tests** - Ensure refactoring doesn't break functionality

Would you like me to help implement any of these improvements?
