import json

test_contact = {
        'username'   : 'test_contact',
        'emails'     : [{'address' : 'test@contact.com'}],
        'first_name' : 'Test',
        'surname'    : 'Contact',
    }

test_contact_2 = {
        'username'   : 'test_contact_2',
        'emails'     : [{'address' : 'test@contact2.com'}],
        'first_name' : 'Test 2',
        'surname'    : 'Contact 2',
    }


def create_contact(client, contact=test_contact):
    return client.post('/contacts',
                       data=json.dumps(contact),
                       content_type='application/json')


def test_create_contact(client):
    assert create_contact(client).status_code == 200


def test_create_contact_missing_data(client):
    test_contact_incomplete = {
        'username'   : 'test_contact',
        'surname'    : 'Contact',
    }
    assert create_contact(client,
                          contact=test_contact_incomplete).status_code == 400


def test_show_contact(client):
    assert client.get(
            '/contacts/%s' % test_contact['username']).status_code == 404
    
    create_contact(client);
    response = client.get('/contacts/%s' % test_contact['username'])

    assert response.status_code == 200
    assert response.json['username'] == test_contact['username']
    assert response.json['emails'] == test_contact['emails']
    assert response.json['first_name'] == test_contact['first_name']
    assert response.json['surname'] == test_contact['surname']

    response = client.get('/contacts/%s' % test_contact['emails'][0]['address'])

    assert response.status_code == 200
    assert response.json['username'] == test_contact['username']
    assert response.json['emails'] == test_contact['emails']
    assert response.json['first_name'] == test_contact['first_name']
    assert response.json['surname'] == test_contact['surname']


def test_update_contact(client):
    create_contact(client)
    response = client.put('/contacts/%s' % test_contact['username'],
                          data=json.dumps(test_contact_2),
                          content_type='application/json')
    assert response.status_code == 200

    response = client.get('/contacts/%s' % test_contact['username'])
    assert response.status_code == 404

    response = client.get('/contacts/%s' % test_contact_2['username'])
    assert response.status_code == 200
    assert response.json['username'] == test_contact_2['username']
    assert response.json['emails'] == test_contact_2['emails']
    assert response.json['first_name'] == test_contact_2['first_name']
    assert response.json['surname'] == test_contact_2['surname']


def test_delete_contact(client):
    create_contact(client);
    assert client.delete(
            '/contacts/%s' % test_contact['username']).status_code == 200

    assert client.get('/contacts/%s' % test_contact['username']).status_code == 404


def test_list_contacts(client, app):
    response = client.get('/contacts')

    assert response.status_code == 200
    assert response.json == {'contacts': []}

    create_contact(client)
    response = client.get('/contacts')

    assert response.status_code == 200
    assert response.json == {'contacts': [test_contact]}

    create_contact(client, contact=test_contact_2)
    response = client.get('/contacts')

    assert response.status_code == 200
    assert response.json == {'contacts': [test_contact, test_contact_2]}
