(function( Eureka, $, undefined ) {

    // Article modal

    var _ArticleModal = React.createClass({

        // Handlers

        handleSubmit: function(e) {
            e.preventDefault();
            //
            var text = this.refs.text.value.trim();
            //
            if ( ! text )
                return;
            //
            var article_data = {
                text: text
            };
            //
            if ( this.props.submitHandler )
                this.props.submitHandler(article_data);
        },

        // Draw

        render: function() {
            return (
                <div
                    id={this.props.modal_id}
                    role='dialog'
                    className='modal fade'
                    tabIndex='-1'
                >
                <div className='modal-dialog'>
                <div className='modal-content'>
                    <div className='modal-header'>
                        <button
                            type="button"
                            className="close"
                            data-dismiss="modal"
                            aria-label="Close"
                        >
                            <span aria-hidden="true">&times;</span>
                        </button>
                        <h4 className='modal-title'>
                            {this.props.title}
                        </h4>
                    </div>
                    <div className='modal-body'>
                        <form
                            className='eureka-atricle-form'
                            onSubmit={this.handleSubmit}
                        >
                            <div className='form-group'>
                                <textarea
                                    rows='10'
                                    ref='text'
                                    className='form-control'
                                    placeholder="Idea!"
                                />
                            </div>
                            <button
                                type='submit'
                                className='btn btn-default'
                            >
                                {this.props.button_text}
                            </button>
                        </form>
                    </div>
                </div>
                </div>
                </div>
            );
        }
    });


    // Articles

    Eureka.Articles = React.createClass({

        // Init

        getInitialState: function() {
            return {
                articles: []
            };
        },

        componentDidMount: function() {
            this.fetchArticles();
        },

        componentWillUnmount: function() {
        },

        // REST

        fetchArticles: function() {
            var url = '/api/article/';
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                cache: false,
                success: function(data) {
                    this.setState({articles: data.objects});
                }.bind(this),
                error: function(xhr, status, err) {
                    // show error
                    console.error(url, status, err.toString());
                }.bind(this)
            });
        },

        // Handlers

        handlePostArticle: function(article_data) {
            var url = '/api/article/';
            // add token directly
            article_data['auth_token'] = $.cookie('auth_token');
            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(article_data),
                dataType: 'json',
                success: function(data) {
                    $('#eureka-modal-article-post').modal('hide');
                    this.fetchArticles();
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(url, xhr.responseJSON);
                }.bind(this)
            });
        },

        // Draw

        render: function() {
            var articles = this.state.articles.map(function(article) {
                return (
                    <blockquote key={article.id}>
                        <p>{article.text}</p>
                        <footer>#{article.id} by {article.auth_email}</footer>
                    </blockquote>
                );
            });
            //
            return (
                <div className='eureka-article'>

                    {articles}

                    <_ArticleModal
                        title='Eureka: Post idea!'
                        button_text='Post'
                        modal_id='eureka-modal-article-post'
                        submitHandler={this.handlePostArticle}
                    />
                </div>
            );
        }
    });

}( window.Eureka = window.Eureka || {}, jQuery ));
