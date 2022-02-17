from crypt import methods
from unicodedata import category
from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import current_user, login_required
from .. import db,photos
from .forms import UpdateProfile, ItemForm, CommentForm
from ..models import User, PhotoProfile, AuctionItem,Comment, Downvote, Upvote
from datetime import datetime

import markdown2


@main.route('/', methods = ['GET', 'POST'])
@login_required
def index():
  '''
  view for root page that returns the index page and its data
  '''

  title = 'Home - Welcome to PitchPal'
  user = current_user

  items = AuctionItem.get_items()

  return render_template('index.html', title=title, user=user.username, items=items)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/add-item',methods= ['GET','POST'])
@login_required
def add_item():
    user = current_user
    form = ItemForm()

    if form.validate_on_submit():
        item = AuctionItem(name=form.name.data,description=form.description.data,starting_price=form.startingPrice.data, user_id=user.id)
        item.save_item()
        return redirect(url_for('.index'))
    
    return render_template('new_auction.html', item_form=form)

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def upvote(id):
    pitches = Upvote.get_upvotes(id)
    usr_id = f'{current_user.id}:{id}'
    for auction in auction_items:
        to_string = f'{auction}'
        if usr_id == to_string:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, auction_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def downvote(id):
    auction_items = Downvote.get_downvotes(id)
    usr_id = f'{current_user.id}:{id}'
    for auction in auction_items:
        to_string = f'{auction}'
        if usr_id == to_string:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, auction_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))
    
@main.route('/comment/<int:auction_id>', methods = ['POST','GET'])
@login_required
def comment(auction_id):
    form = CommentForm()
    auction = AuctionItem.query.get(auction_id)
    comments = Comment.query.filter_by(auction_id = auction_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        auction_id = auction_id
        new_comment = Comment(comment = comment,auction_id = auction_id,user=current_user)
        new_comment.save_comment()
        return redirect(url_for('.comment', auction_id = auction_id))
    
    return render_template('comment.html', form =form, auction = auction,comments=comments)
