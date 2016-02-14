(function( Eureka, $, undefined ) {

    // Header

    Eureka.Header = React.createClass({
        // render
        render: function() {
            return (
                <div className='navbar navbar-default navbar-fixed-top' >
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
                            <ul className='nav navbar-nav navbar-right'>
                                <li>
                                    <a href='/signin'>
                                        Sign in / Sign up
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            );
        }
    });

}( window.Eureka = window.Eureka || {}, jQuery ));
