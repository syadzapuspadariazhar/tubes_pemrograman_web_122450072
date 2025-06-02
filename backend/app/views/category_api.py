from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
import transaction
try:
    from ..models import DBSession, Category
except Exception as e:
    print("IMPORT ERROR in category_api.py:", e)
    raise
import json
import logging

print("category_api.py loaded")

logger = logging.getLogger('category_api')

@view_config(route_name='get_categories', renderer='json')
def get_categories(request):
    try:
        logger.info("Getting all categories...")
        # Remove the session and create a fresh query
        DBSession.remove()
        categories = DBSession.query(Category).all()
        logger.info(f"Found {len(categories)} categories")
        result = [dict(id=c.id, nama=c.nama) for c in categories]
        logger.info(f"Returning categories: {result}")
        return result
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        import traceback
        traceback.print_exc()
        return []

@view_config(route_name='add_category', renderer='json')
def add_category(request):
    try:
        # Log the incoming request for debugging
        logger.info(f"Received POST request: Content-Type: {request.content_type}")
        logger.info(f"Request body: {request.body}")
        
        # Check if request has JSON body
        if request.content_type != 'application/json':
            request.response.status = 400
            return dict(error="Invalid content type", message="Content-Type must be application/json")
            
        data = request.json_body
        logger.info(f"Parsed JSON data: {data}")
        
        if 'nama' not in data or not data.get('nama'):
            request.response.status = 400
            return dict(error="Missing field", message="Field 'nama' harus diisi")
        
        # Create new category with proper session handling
        logger.info("Creating new category...")
        
        # Remove any existing session to ensure clean state
        DBSession.remove()
        
        new_cat = Category(nama=data.get('nama'))
        
        logger.info("Adding to session...")
        DBSession.add(new_cat)
        
        logger.info("Flushing to get ID...")
        DBSession.flush()  # This will assign the ID without committing
        
        logger.info("Committing session...")
        DBSession.commit()
        
        # Force session removal to ensure other requests see the changes
        DBSession.remove()
        
        logger.info(f"Category created with ID: {new_cat.id}")
        return dict(message="Kategori berhasil ditambahkan", id=new_cat.id)
        
    except Exception as e:
        logger.error(f"Error in add_category: {e}")
        import traceback
        traceback.print_exc()
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))

@view_config(route_name='update_category', renderer='json')
def update_category(request):
    try:
        id = int(request.matchdict['id'])
        data = request.json_body
        
        DBSession.remove()  # Clean session
        cat = DBSession.query(Category).get(id)
        if not cat:
            request.response.status = 404
            return dict(error="Kategori tidak ditemukan")
        
        cat.nama = data.get('nama', cat.nama)
        DBSession.commit()
        DBSession.remove()  # Clean session after commit
        
        return dict(message="Kategori diperbarui")
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))

@view_config(route_name='delete_category', renderer='json')
def delete_category(request):
    try:
        id = int(request.matchdict['id'])
        DBSession.remove()  # Clean session
        cat = DBSession.query(Category).get(id)
        if not cat:
            request.response.status = 404
            return dict(error="Kategori tidak ditemukan")
        DBSession.delete(cat)
        DBSession.commit()
        DBSession.remove()  # Clean session after commit
        return dict(message="Kategori dihapus")
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))