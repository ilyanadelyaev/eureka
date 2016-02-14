(function( Eureka, $, undefined ) {

    // Header

    Eureka.Header = React.createClass({
        render: function() {
            return (
                <div className='eureka-header navbar navbar-default navbar-fixed-top' >
                    <div className='container-fluid'>
                        <div className='navbar-header'>
                            <a href='/' className='navbar-brand'>
                                Eureka
                            </a>
                        </div>
                        <div
                            id='navbar'
                            className='collapse navbar-collapse'
                        >
                            {this.props.auth_block}
                        </div>
                    </div>
                </div>
            );
        }
    });

}( window.Eureka = window.Eureka || {}, jQuery ));
