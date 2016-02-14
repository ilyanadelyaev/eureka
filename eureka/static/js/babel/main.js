// Application

var Application = React.createClass({
    render: function() {
        var auth_block = (
            <Eureka.AuthHeaderBlock
                ref="auth_header_block"
            />
        );
        return (
            <div className='eureka-application container'>
                <Eureka.Header
                    auth_block={auth_block}
                />
                <Eureka.Auth
                    parent_node={this}
                />
                <Eureka.Articles />
            </div>
        );
    }
});


// Run

ReactDOM.render(
    <Application />,
    document.getElementById('application')
);
