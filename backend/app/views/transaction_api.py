from pyramid.view import view_config
from pyramid.response import Response
from ..models import DBSession, Transaction
from datetime import datetime
import logging

logger = logging.getLogger('transaction_api')

@view_config(route_name='get_transactions', renderer='json')
def get_transactions(request):
    try:
        logger.info("Getting all transactions...")
        # Remove the session and create a fresh query
        DBSession.remove()
        transactions = DBSession.query(Transaction).all()
        logger.info(f"Found {len(transactions)} transactions")
        result = [
            dict(
                id=t.id,
                deskripsi=t.deskripsi,
                jumlah=t.jumlah,
                jenis=t.jenis,
                tanggal=t.tanggal.isoformat(),
                kategori_id=t.kategori_id
            ) for t in transactions
        ]
        logger.info(f"Returning transactions: {len(result)} items")
        return result
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        import traceback
        traceback.print_exc()
        return []

@view_config(route_name='add_transaction', renderer='json')
def add_transaction(request):
    try:
        # Log the incoming request for debugging
        logger.info(f"Received POST request for transaction: {request.body}")
        
        data = request.json_body
        logger.info(f"Parsed JSON data: {data}")
        
        # Remove any existing session to ensure clean state
        DBSession.remove()
          # Create new transaction with proper session handling
        logger.info("Creating new transaction...")
        t = Transaction(
            deskripsi=data['deskripsi'],
            jumlah=data['jumlah'],
            jenis=data['jenis'],
            tanggal=datetime.fromisoformat(data['tanggal']),
            kategori_id=data['kategori_id']
        )
        
        logger.info("Adding to session...")
        DBSession.add(t)
        logger.info(f"Transaction before flush - ID: {t.id}")
        
        logger.info("Flushing to get ID...")
        DBSession.flush()  # This will assign the ID without committing
        logger.info(f"Transaction after flush - ID: {t.id}")
        
        logger.info("Committing session...")
        DBSession.commit()
        logger.info(f"Transaction after commit - ID: {t.id}")
        
        # Force session removal to ensure other requests see the changes
        DBSession.remove()
        
        logger.info(f"Transaction created with ID: {t.id}")
        return dict(message="Transaksi ditambahkan", id=t.id)
        
    except Exception as e:
        logger.error(f"Error in add_transaction: {e}")
        import traceback
        traceback.print_exc()
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))

@view_config(route_name='update_transaction', renderer='json')
def update_transaction(request):
    try:
        logger.info(f"Updating transaction: {request.matchdict['id']}")
        
        # Remove any existing session to ensure clean state
        DBSession.remove()
        
        id = int(request.matchdict['id'])
        data = request.json_body
        logger.info(f"Update data: {data}")
        
        t = DBSession.query(Transaction).get(id)
        if not t:
            logger.warning(f"Transaction {id} not found")
            request.response.status = 404
            return dict(error="Transaksi tidak ditemukan")
        
        # Update the transaction fields
        t.deskripsi = data['deskripsi']
        t.jumlah = data['jumlah']
        t.jenis = data['jenis']
        t.tanggal = datetime.fromisoformat(data['tanggal'])
        t.kategori_id = data['kategori_id']
        
        logger.info("Committing updates...")
        DBSession.commit()
        
        # Force session removal to ensure other requests see the changes
        DBSession.remove()
        
        logger.info(f"Transaction {id} updated successfully")
        return dict(message="Transaksi diperbarui")
        
    except Exception as e:
        logger.error(f"Error updating transaction: {e}")
        import traceback
        traceback.print_exc()
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))

@view_config(route_name='delete_transaction', renderer='json')
def delete_transaction(request):
    try:
        logger.info(f"Deleting transaction: {request.matchdict['id']}")
        
        # Remove any existing session to ensure clean state
        DBSession.remove()
        
        id = int(request.matchdict['id'])
        t = DBSession.query(Transaction).get(id)
        if not t:
            logger.warning(f"Transaction {id} not found")
            request.response.status = 404
            return dict(error="Transaksi tidak ditemukan")
        
        logger.info(f"Deleting transaction: {t.deskripsi}")
        DBSession.delete(t)
        
        logger.info("Committing deletion...")
        DBSession.commit()
          # Force session removal to ensure other requests see the changes
        DBSession.remove()
        
        logger.info(f"Transaction {id} deleted successfully")
        return dict(message="Transaksi dihapus")
        
    except Exception as e:
        logger.error(f"Error deleting transaction: {e}")
        import traceback
        traceback.print_exc()
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass
        request.response.status = 500
        return dict(error="Server error", message=str(e))