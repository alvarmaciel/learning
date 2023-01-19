from pytest_bdd import scenario, given, when, then


@given("a user with permissions")
def step_impl():
    raise NotImplementedError(u'STEP: Given a user with permissions')


@when("post a graphql mutation")
def step_impl():
    raise NotImplementedError(u'STEP: When post a graphql mutation')


@then("a new associated is created in DB")
def step_impl():
    raise NotImplementedError(u'STEP: Then a new associated is created in DB')


@then("the mutation responds with the new socie")
def step_impl():
    raise NotImplementedError(u'STEP: Then the mutation responds with the new socie')