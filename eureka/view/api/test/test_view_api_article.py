import eureka.model.auth
import eureka.model.article


class TestAPIArticle:
    @staticmethod
    def __create_auth(session_scope, email, auth_token=None):
        """
        auth creation helper
        """
        _auth_id = None
        with session_scope() as session:
            # clear table
            eureka.model.auth.AuthUser.query.delete()
            #
            auth = eureka.model.auth.AuthUser(
                email=email,
                auth_token=auth_token,
            )
            session.add(auth)
            session.flush()
            _auth_id = auth.id
        return _auth_id

    @staticmethod
    def __create_article(session_scope, auth_id, text):
        """
        article creation helper
        """
        _article_id = None
        with session_scope() as session:
            # clear table
            eureka.model.article.Article.query.delete()
            #
            article = eureka.model.article.Article(
                auth_id=auth_id,
                text=text,
            )
            session.add(article)
            session.flush()
            _article_id = article.id
        return _article_id

    def test__article__post_201(
            self, web_app, session_scope,
            controller, email, article_text,
    ):
        """
        Create - OK
        """
        auth_token = 'token'
        auth_id = self.__create_auth(session_scope, email, auth_token)
        #
        resp = web_app.post_json(
            '/api/article/',
            {'auth_token': auth_token, 'text': article_text},
            expect_errors=True
        )
        assert resp.status_code == 201
        #
        obj = controller.article.one(resp.json['id'])
        #
        assert obj['auth_email'] == email
        assert obj['auth_id'] == auth_id
        assert obj['text'] == article_text

    def test__article__post_404(
            self, web_app,
            session_scope, email, article_text
    ):
        """
        Create - Error
        """
        resp = web_app.post_json(
            '/api/article/',
            {},
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Invalid data'

    def test__articless__get_list_200(
            self, web_app,
            session_scope, email, article_text,
    ):
        """
        Get all - OK
        """
        auth_id = self.__create_auth(session_scope, email)
        self.__create_article(session_scope, auth_id, article_text)
        #
        resp = web_app.get(
            '/api/article/',
        )
        assert resp.status_code == 200
        #
        assert resp.json['count'] == 1
        assert resp.json['objects'][0]['auth_email'] == email
        assert resp.json['objects'][0]['auth_id'] == auth_id
        assert resp.json['objects'][0]['text'] == article_text

    def test__article__get_200(
            self, web_app,
            session_scope, email, article_text,
    ):
        """
        Read - OK
        """
        auth_id = self.__create_auth(session_scope, email)
        _article_id = self.__create_article(
            session_scope, auth_id, article_text)
        #
        resp = web_app.get(
            '/api/article/{}/'.format(_article_id),
        )
        assert resp.status_code == 200
        #
        assert resp.json['auth_email'] == email
        assert resp.json['auth_id'] == auth_id
        assert resp.json['text'] == article_text

    def test__article__get_404(
            self, web_app,
    ):
        """
        Read - Not found
        """
        resp = web_app.get(
            '/api/article/a/',
            expect_errors=True
        )
        assert resp.status_code == 404
        #
        resp = web_app.get(
            '/api/article/0/',
            expect_errors=True
        )
        assert resp.status_code == 404
        assert resp.json['error'] == \
            'Article "0" is not exists'
