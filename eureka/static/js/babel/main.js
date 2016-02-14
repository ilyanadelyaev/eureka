// Application

var Application = React.createClass({
    render: function() {
        return (
            <div className='eureka-application container'>
                <Eureka.Header
                    auth_block=<Eureka.AuthHeaderBlock />
                />
                <Eureka.Auth
                    parent_node={this}
                />
            </div>
        );
    }
});


// Run

ReactDOM.render(
    <Application />,
    document.getElementById('application')
);
