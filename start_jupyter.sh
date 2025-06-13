#!/bin/bash

echo "🚀 Starting Jupyter Lab for Neptune Analytics Graph Visualization"
echo "=================================================="

# Activate virtual environment
source neptune_env/bin/activate

echo "📊 Available notebooks:"
echo "  • neptune_graph_viz_complete.ipynb - Complete graph visualization"
echo "  • neptune_analytics_working.ipynb - Basic analytics"
echo ""

echo "🌐 Starting Jupyter Lab..."
echo "💡 The notebook will open in your browser automatically"
echo "🔗 If it doesn't open, go to: http://localhost:8888"
echo ""
echo "Press Ctrl+C to stop Jupyter when done"
echo ""

# Start Jupyter Lab
jupyter lab --no-browser --port=8888 --ip=127.0.0.1
