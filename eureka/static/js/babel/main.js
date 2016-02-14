// Application

var Application = React.createClass({
    render: function() {
        return (
            <div className='eureka-application container'>
                <Eureka.Header
                    article_block=<Eureka.ArticleHeaderBlock />
                    auth_block=<Eureka.AuthHeaderBlock
                        ref="auth_header_block"
                    />
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
