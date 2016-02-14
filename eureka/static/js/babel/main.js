var Application = React.createClass({
    render: function() {
        return (
            <div>
                <Eureka.Header />
                <div className='container-fluid'>
                    <h1>Test</h1>
                </div>
            </div>
        );
    }
});


// Run

ReactDOM.render(
    <Application />,
    document.getElementById('application')
);
