import pytest
import tests.common as common
import nomad
import nomad.api.exceptions
import json
import responses

@pytest.fixture
def nomad_setup():
    n = nomad.Nomad(host=common.IP, port=common.NOMAD_PORT)
    return n


# integration tests requires nomad Vagrant VM or Binary running
def test_register_job(nomad_setup):

    with open("example.json") as fh:
        job = json.loads(fh.read())
        nomad_setup.job.register_job("example", job)
        assert "example" in nomad_setup.job


def test_ls_list_files(nomad_setup):
    """Use Functioncal Test Instead"""
    # test_register_job(nomad_setup)
    #
    # a = nomad_setup.allocations.get_allocations()[0]["ID"]
    # f = nomad_setup.client.ls.list_files(a)


def test_stat_stat_file(nomad_setup):
    """Use Functioncal Test Instead"""
    # test_register_job(nomad_setup)
    #
    # a = nomad_setup.allocations.get_allocations()[0]["ID"]
    # f = nomad_setup.client.stat.stat_file(a)


def test_cat_read_file(nomad_setup):
    """Use Functioncal Test Instead"""
    # test_register_job(nomad_setup)
    #
    # a = nomad_setup.allocations.get_allocations()[0]["ID"]
    # f = nomad_setup.client.cat.read_file(a,"/redis/redis-executor.out")


def test_dunder_str(nomad_setup):
    assert isinstance(str(nomad_setup.client), str)
    assert isinstance(str(nomad_setup.client.ls), str)
    assert isinstance(str(nomad_setup.client.cat), str)
    assert isinstance(str(nomad_setup.client.stat), str)


def test_dunder_repr(nomad_setup):
    assert isinstance(repr(nomad_setup.client), str)
    assert isinstance(repr(nomad_setup.client.ls), str)
    assert isinstance(repr(nomad_setup.client.cat), str)
    assert isinstance(repr(nomad_setup.client.stat), str)


def test_dunder_getattr(nomad_setup):

    with pytest.raises(AttributeError):
        d = nomad_setup.client.does_not_exist

    with pytest.raises(AttributeError):
        d = nomad_setup.client.ls.does_not_exist

    with pytest.raises(AttributeError):
        d = nomad_setup.client.cat.does_not_exist

    with pytest.raises(AttributeError):
        d = nomad_setup.client.stat.does_not_exist


# Mocking tests
@responses.activate
def test_mock_client_ls_not_found(nomad_setup):
    responses.add(responses.GET,
                  "http://{0}:{1}/v1/client/fs/ls/NOT-A-REAL-ALLOCATION-ID".format(common.IP,common.NOMAD_PORT),
                  status=500,
                  content_type="text/plain")

    with pytest.raises(nomad.api.exceptions.URLNotFoundNomadException):
        nomad_setup.client.ls.list_files("NOT-A-REAL-ALLOCATION-ID")

@responses.activate
def test_mock_client_ls_found(nomad_setup):
    responses.add(responses.GET,
                  "http://{0}:{1}/v1/client/fs/ls/REAL-ALLOCATION-ID".format(common.IP,common.NOMAD_PORT),
                  status=200,
                  content_type="application/json",
                  body=common.CLIENT_LS)


    isinstance(nomad_setup.client.ls.list_files("REAL-ALLOCATION-ID"),list)


@responses.activate
def test_mock_client_stat_not_found(nomad_setup):
    responses.add(responses.GET,
                  "http://{0}:{1}/v1/client/fs/stat/NOT-A-REAL-ALLOCATION-ID".format(common.IP,common.NOMAD_PORT),
                  status=500,
                  content_type="text/plain")

    with pytest.raises(nomad.api.exceptions.URLNotFoundNomadException):
        nomad_setup.client.stat.stat_file("NOT-A-REAL-ALLOCATION-ID")

@responses.activate
def test_mock_client_stat_found(nomad_setup):
    responses.add(responses.GET,
                  "http://{0}:{1}/v1/client/fs/stat/REAL-ALLOCATION-ID".format(common.IP,common.NOMAD_PORT),
                  status=200,
                  content_type="application/json",
                  body=common.CLIENT_STAT)


    isinstance(nomad_setup.client.stat.stat_file("REAL-ALLOCATION-ID"),dict)
