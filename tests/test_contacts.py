import json

test_contact = {
        'username'   : 'test_contact',
        'email'      : 'test@contact.com',
        'first_name' : 'Test',
        'surname'    : 'Contact',
    }

test_contact_2 = {
        'username'   : 'test_contact_2',
        'email'      : 'test@contact_2.com',
        'first_name' : 'Test 2',
        'surname'    : 'Contact 2',
    }


def create_contact(client, contact=test_contact):
    return client.post('/contacts',
                       data=json.dumps(contact),
                       content_type='application/json')


def test_create_contact(client):
    assert create_contact(client).status_code == 200

    
def test_show_contact(client):
    create_contact(client);
    response = client.get('/contacts/%s' % test_contact['username'])

    assert response.status_code == 200
    assert response.json['username'] == test_contact['username']
    assert response.json['email'] == test_contact['email']
    assert response.json['first_name'] == test_contact['first_name']
    assert response.json['surname'] == test_contact['surname']


def test_list_contacts(client, app):
    response = client.get('/contacts')

    assert response.status_code == 200
    assert response.json == {'contacts': []}
