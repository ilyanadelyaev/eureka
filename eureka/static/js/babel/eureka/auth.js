(function( Eureka, $, undefined ) {

    // Error message

    var __show_error = function( error_message, modal_id ) {
        ReactDOM.render(
            <_ErrorMessage
                title='Auth error'
                error_message={error_message}
            />,
            document.getElementById(modal_id)
        );
    };

    var _ErrorMessage = React.createClass({
        render: function() {
            return (
                <div
                    className='alert alert-danger alert-dismissible fade in'
                    role='alert'
                >
                    <button
                        type='button'
                        className='close'
                        data-dismiss='alert'
                        aria-label='Close'
                    >
                        <span aria-hidden='true'>&times;</span>
                    </button>
                    <h4>
                        {this.props.title}
                    </h4>
                    <p>
                        {this.props.error_message}
                    </p>
                </div>
            );
        }
    });


    // Auth header

    Eureka.AuthHeaderBlock = React.createClass({

        // Handlers

        handleUser: function(e) {
            e.preventDefault();
        },

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
                                href='#'
                            >
                                Sign up
                            </a>
                        </li>
                        <li>
                            <a
                                data-toggle='modal'
                                data-target='#eureka-modal-auth-signin'
                                href='#'
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
                            <a
                                data-toggle='modal'
                                data-target='#eureka-modal-article-post'
                                href='#'
                            >
                                Post
                            </a>
                        </li>
                        <li>
                            <a
                                onClick={this.handleUser}
                                href='#'
                            >
                                {$.cookie('auth_email')}
                            </a>
                        </li>
                        <li>
                            <a
                                onClick={this.handleLogOut}
                                href='#'
                            >
                                Log out
                            </a>
                        </li>
                    </ul>
                );
            }
        }
    });


    // Auth modal

    var _AuthModal = React.createClass({

        // Handlers

        handleSubmit: function(e) {
            e.preventDefault();
            //
            var email = this.refs.auth_email.value.trim();
            var password = this.refs.auth_password.value;
            // email check
            if ( ! email ) {
                $('#' + this.props.modal_id).find('.eureka-auth-email').addClass('has-error');
                return;
            } else {
                $('#' + this.props.modal_id).find('.eureka-auth-email').removeClass('has-error');
            }
            // password check
            if ( ! password ) {
                $('#' + this.props.modal_id).find('.eureka-auth-password').addClass('has-error');
                return;
            } else {
                $('#' + this.props.modal_id).find('.eureka-auth-password').removeClass('has-error');
            }
            // password repeat check
            if ( this.props.password_repeat ) {
                var password_repeat = this.refs.auth_password_repeat.value;
                if ( password != password_repeat ) {
                    $('#' + this.props.modal_id).find('.eureka-auth-password').addClass('has-error');
                    $('#' + this.props.modal_id).find('.eureka-auth-password-repeat').addClass('has-error');
                    return;
                } else {
                    $('#' + this.props.modal_id).find('.eureka-auth-password').removeClass('has-error');
                    $('#' + this.props.modal_id).find('.eureka-auth-password-repeat').removeClass('has-error');
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
                    <div className='form-group eureka-auth-password-repeat'>
                        <label htmlFor='eureka-auth-password-repeat'>
                            Repeat password
                        </label>
                        <input
                            type='password'
                            id='eureka-auth-password-repeat'
                            ref='auth_password_repeat'
                            className='form-control'
                            placeholder="********"
                        />
                    </div>
                );
            }
            //
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
                            className='eureka-auth-form'
                            onSubmit={this.handleSubmit}
                        >
                            <div className='form-group eureka-auth-email'>
                                <label htmlFor='eureka-auth-email'>
                                    Email address
                                </label>
                                <input
                                    type='email'
                                    id='eureka-auth-email'
                                    ref='auth_email'
                                    className='form-control'
                                    placeholder="mail@example.com"
                                />
                            </div>
                            <div className='form-group eureka-auth-password'>
                                <label htmlFor='eureka-auth-password'>
                                    Password
                                </label>
                                <input
                                    type='password'
                                    id='eureka-auth-password'
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
                    </div>
                    <div id={this.props.modal_id + '-error'}></div>
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
                    this.props.parent_node.refs.auth_header_block.forceUpdate();
                }.bind(this),
                error: function(xhr, status, err) {
                    __show_error(xhr.responseJSON.error, 'eureka-modal-auth-signup-error');
                    console.error(url, xhr.responseJSON);
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
                    __show_error(xhr.responseJSON.error, 'eureka-modal-auth-signin-error');
                    console.error(url, xhr.responseJSON);
                }.bind(this)
            });
        },

        // Draw

        render: function() {
            return (
                <div className='eureka-auth'>
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
