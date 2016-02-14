(function( Eureka, $, undefined ) {

    // Header

    Eureka.Header = React.createClass({
        render: function() {
            return (
                <div className='eureka-header navbar navbar-default navbar-fixed-top' >
                    <button
                        type='button'
                        className='navbar-toggle collapsed'
                        data-toggle='collapse'
                        data-target='#eureka-navbar-collapse-1'
                        aria-expanded='false'
                    >
                        <span className='sr-only'>Toggle navigation</span>
                        <span className='icon-bar'></span>
                        <span className='icon-bar'></span>
                        <span className='icon-bar'></span>
                    </button>
                    <div className='container-fluid'>
                        <div className='navbar-header'>
                            <a href='/' className='navbar-brand'>
                                Eureka
                            </a>
                        </div>
                        <div
                            id="eureka-navbar-collapse-1"
                            className='collapse navbar-collapse'
                        >
                            {this.props.article_block}
                            {this.props.auth_block}
                        </div>
                    </div>
                </div>
            );
        }
    });

}( window.Eureka = window.Eureka || {}, jQuery ));
