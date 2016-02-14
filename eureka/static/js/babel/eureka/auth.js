(function( Eureka, $, undefined ) {

    // Auth header

    Eureka.AuthHeaderBlock = React.createClass({
        handleLogOut: function(e) {
            e.preventDefault();
            //
            $.removeCookie('auth_email');
            $.removeCookie('auth_token');
            // update state
            this.forceUpdate();
        },

        // render
        render: function() {
            if ( ! $.cookie('auth_email') ) {
                return (
                    <ul className='nav navbar-nav navbar-right'>
                        <li>
                            <a
                                data-toggle='modal'
                                data-target='#eureka-modal-auth-signup'
                            >
                                Sign up
                            </a>
                        </li>
                        <li>
                            <a
                                data-toggle='modal'
                                data-target='#eureka-modal-auth-signin'
                            >
                                Sign in
                            </a>
                        </li>
                    </ul>
                );
            } else {
                return (
                    <ul className='nav navbar-nav navbar-right'>
                        <li>
                            <a>
                                {$.cookie('auth_email')}
                            </a>
                        </li>
                        <li>
                            <a
                                onClick={this.handleLogOut}
                            >
                                Log out
                            </a>
                        </li>
                    </ul>
                );
            }
        }
    });


    // Auth form

    var _AuthForm = React.createClass({

        // Init

        getInitialState: function() {
            return {
                password_error: ''
            };
        },

        // Handlers

        handleSubmit: function(e) {
            e.preventDefault();
            //
            var email = this.refs.auth_email.value.trim();
            var password = this.refs.auth_password.value;
            //
            if ( ! email || ! password )
                return;
            if ( this.props.password_repeat ) {
                var password_repeat = this.refs.auth_password_repeat.value;
                if ( password != password_repeat ) {
                    this.setState({password_error: 'Passwords not equal'});
                    return;
                }
            }
            //
            var auth_data = {
                email: email,
                password: password
            };
            //
            if ( this.props.submitHandler )
                this.props.submitHandler(auth_data);
        },

        // Draw

        render: function() {
            var password_repeat = null;
            if ( this.props.password_repeat ) {
                password_repeat = (
                    <div className='form-group'>
                        <label htmlFor='auth_password_repeat'>
                            Repeat password
                        </label>
                        <input
                            type='password'
                            id='auth_password_repeat'
                            ref='auth_password_repeat'
                            className='form-control'
                            placeholder="********"
                        />
                        <div
                            className='alert alert-danger'
                        >
                            {this.state.password_error}
                        </div>
                    </div>
                );
            }
            return (
                <form
                    className='eureka-auth-form'
                    onSubmit={this.handleSubmit}
                >
                    <div className='form-group'>
                        <label htmlFor='auth_email'>
                            Email address
                        </label>
                        <input
                            type='email'
                            id='auth_email'
                            ref='auth_email'
                            className='form-control'
                            placeholder="mail@example.com"
                        />
                    </div>
                    <div className='form-group'>
                        <label htmlFor='auth_password'>
                            Password
                        </label>
                        <input
                            type='password'
                            id='auth_password'
                            ref='auth_password'
                            className='form-control'
                            placeholder="********"
                        />
                    </div>
                    {password_repeat}
                    <button
                        type='submit'
                        className='btn btn-default'
                    >
                        {this.props.button_text}
                    </button>
                </form>
            );
        }
    });


    // Auth modal

    var _AuthModal = React.createClass({
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
                        <_AuthForm
                            button_text={this.props.button_text}
                            password_repeat={this.props.password_repeat}
                            submitHandler={this.props.submitHandler}
                        />
                        {this.props.children}
                    </div>
                </div>
                </div>
                </div>
            );
        }
    });


    // Auth

    Eureka.Auth = React.createClass({

        // Init

        getInitialState: function() {
            return {
                auth_data: {}
            };
        },

        // Handlers

        handleSignUp: function(auth_data) {
            var url = '/api/auth/signup';
            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(auth_data),
                dataType: 'json',
                success: function(data) {
                    $('#eureka-modal-auth-signup').modal('hide');
                    this.props.parent_node.forceUpdate();
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(url, status, err.toString());
                }.bind(this)
            });
        },

        handleSignIn: function(auth_data) {
            var url = '/api/auth/signin';
            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(auth_data),
                dataType: 'json',
                success: function(data) {
                    $('#eureka-modal-auth-signin').modal('hide');
                    this.props.parent_node.refs.auth_header_block.forceUpdate();
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(url, status, err.toString());
                }.bind(this)
            });
        },

        // Draw

        render: function() {
            return (
                <div className='eureka-auth-modals'>
                    <_AuthModal
                        title='Eureka: Sign up'
                        button_text='Sign up'
                        password_repeat={true}
                        modal_id='eureka-modal-auth-signup'
                        submitHandler={this.handleSignUp}
                    />

                    <_AuthModal
                        title='Eureka: Sign in'
                        button_text='Sign in'
                        modal_id='eureka-modal-auth-signin'
                        submitHandler={this.handleSignIn}
                    />
                </div>
            );
        }
    });

}( window.Eureka = window.Eureka || {}, jQuery ));
