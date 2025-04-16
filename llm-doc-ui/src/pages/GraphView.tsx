const GraphView = () => {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">🔗 Relationship Graph</h1>
        <iframe
          src="http://localhost:8000/static/relationship_graph.html"
          className="w-full h-[700px] border rounded-lg shadow"
          title="Graph View"
        />
      </div>
    );
  };
  
  export default GraphView;