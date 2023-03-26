session['user_id'] = None
session['page_views'] = None

# ============= give permission to access certain routes ============= 
# check whether log in or not before any action
# will run this hook first before session["user_id"] obj does anything
@app.before_request
def check_id_logged_in:
    if not session["user_id"]:
        return {"error": "Unauthorized"}, 401


class Document(Resource):
    def get(self, id):
        # ====================================================================================
        # documents should only be shown to users when they're logged in.
        # if not session["user_id"]:
        #     return make_response({'error': "Unauthorized"}, 401)
        # =================== move inside befre_request decorator function ===================

        document = Document.query.filter(Document.id).first()
        return document.to_dict()
    

    def patch(self, id):
        if not session["user_id"]:
            return make_response({'error': "Unauthorized"}, 401)
        document = Document.query.filter(Document.id).first()
        for attr in request.get_json():
            setattr(document, attr, request.get_json()[attr])
        db.session.add(document)
        db.session.commit()
        return make_response(document.to_dict(), 200)
    
    def delete(self, id):
        if not session["user_id"]:
            return make_response({'error': "Unauthorized"}, 401)
        document = Document.query.filter(Document.id).first()
        db.session.delete(document)
        db.session.commit()
        return make_response({"message": "Deleted!"}, 200)

class DocumentList(Resource):
    def get(self):
        documents = Document.query.all()
        return [document.to_dict() for document in documents]

api.add_resource(Document, '/documents/<int:id>', endpoint='document')
api.add_resource(DocumentList, '/documents', endpoint='document_list')
# for Document, ignore 
# ============= ============= ============= ============= ===


# ============= show only three articles ============= 
class showArticle(Resource):
    def get(self, id):
        # the first request, set value for session "page_views" if False, else get the value
        session["page_views"] = 0 for not session.get("page_views") else session.get("page_views")
        # set to one
        session.["page_views"] += 1

        if session["page_views"] <= 3:
            article_dict = Article.query.filter(Article.id=id).first().to_dict()
            return make_response(article_dict, 200)
api.add_resource()
# ============= ============= ============= ============= ===

# ============= login and persist logging in ================
class Login(Resource):
    def post(self):
        user = User.query.filter(User.username==request.get_json("username")).first()

        session["user_id"] = user.id
        return make_response(user.to_dict(), 200)

class CheckSession(Resource):
    def get(self):
        user = User.wuery.filter(User.id==sessionp['user_id']).first()

        if not user:
            # the client request has not been completed 
            # because it lacks valid authentication credentials for the requested resource
            return make_response({'message': "401: Not Authorized"}, 401)
        return make_response(user.to_dict(), 200)

api.add_resource(Login, '/login')
app.add_resource(CheckSession, '/check_session')
# ==============================================================

# ================== Log out user ==============================
class Logout(Resource):
    session["user_id"] = None
    return make_response(jsonify({"message", "204: No Content, please login agian"}), 204)
api.add_resource(Logout, '/logout')    
# ==============================================================