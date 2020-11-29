import os
import ckanapi
import requests


class OpanAfricaUploader(object):
  def __init__(self, api_key):
    """Constructor

    Args:
        api_key (string): CKAN api key
    """
    self.data_portal = 'https://africaopendata.org'
    self.APIKEY = api_key
    self.ckan = ckanapi.RemoteCKAN(self.data_portal, apikey=self.APIKEY)

  def create_package(self, org, url, title):
    """create new package if it does not exist yet.

    Args:
        url (str): the url of package eg. https://open.africa/dataset/{package url}
        title (str): the title of package
    """
    package_name = url
    package_title = title
    organization_name = org
    try:
        print ('Creating "{package_title}" package'.format(**locals()))
        self.package = self.ckan.action.package_create(name=package_name,
                                            title=package_title,
                                            owner_org = organization_name)
    except (ckanapi.ValidationError) as e:
        if (e.error_dict['__type'] == 'Validation Error' and
          e.error_dict['name'] == ['That URL is already in use.']):
            print ('"{package_title}" package already exists'.format(**locals()))
            self.package = self.ckan.action.package_show(id=package_name)
        else:
            raise

  def resource_create(self, data, path, api="/api/action/resource_create"):
    """create new resource, or update existing resource

    Args:
        data (object): data for creating resource. data must contain package_id, name, format, description. If you overwrite existing resource, id also must be included.
        path (str): file path for uploading
        api (str, optional): API url for creating or updating. Defaults to "/api/action/resource_create". If you want to update, please specify url for "/api/action/resource_update"
    """
    self.api_url = self.data_portal + api
    print ('Creating "{}"'.format(data['name']))
    r = requests.post(self.api_url,
                      data=data,
                      headers={'Authorization': self.APIKEY},
                      files=[('upload', open(path, 'rb'))])

    if r.status_code != 200:
        print ('Error while creating resource: {0}'.format(r.content))
    else:
      print ('Uploaded "{}" successfully'.format(data['name']))

  def resource_update(self, data, path):
    """update existing resource

    Args:
        data (object): data for creating resource. data must contain id, package_id, name, format, description.
        path (str): file path for uploading
    """
    self.resource_create(data, path, "/api/action/resource_update")

  def upload_datasets(self, path, description):
    """upload datasets under the package

    Args:
        path (str): file path for uploading
        description (str): description for the dataset
    """
    filename = os.path.basename(path)
    extension = os.path.splitext(filename)[1][1:].lower()
    
    data = {
      'package_id': self.package['id'],
      'name': filename,
      'format': extension,
      'description': description
    }

    resources = self.package['resources']
    if len(resources) > 0:
      target_resource = None
      for resource in reversed(resources):
        if filename == resource['name']:
          target_resource = resource
          break

      if target_resource == None:
        self.resource_create(data, path)
      else:
        print ('Resource "{}" already exists, it will be overwritten'.format(target_resource['name']))
        data['id'] = target_resource['id']
        self.resource_update(data, path)
    else:
      self.resource_create(data, path)
