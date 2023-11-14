%define pypi_name msal

%def_without net_check
%def_without check

Name:    python3-module-%pypi_name
Version: 1.25.0
Release: alt1

Summary: Microsoft Authentication Library (MSAL) for Python
License: MIT
Group:   Development/Python3
URL:     https://github.com/AzureAD/microsoft-authentication-library-for-python

Packager: Danilkin Danila <danild@altlinux.org>

BuildRequires(pre): rpm-build-python3
BuildRequires: python3-module-setuptools
BuildRequires: python3-module-wheel

%if_with check
BuildRequires: python3-module-pytest
BuildRequires: python3-module-requests
BuildRequires: python3-module-jwt
%endif


BuildArch: noarch

Source: %name-%version.tar

%description
The Microsoft Authentication Library for Python enables applications to integrate with the Microsoft identity platform. It allows you to sign in users or apps with Microsoft identities (Azure AD, Microsoft Accounts and Azure AD B2C accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or your own APIs registered with the Microsoft identity platform. It is built using industry standard OAuth2 and OpenID Connect protocols.

%prep
%setup

# - We can’t generate BR’s from a requirements file with “-e .” in it.
# - We don’t need or want to run benchmarks (tests/test_benchmark.py), so don’t
#   generate benchmarking dependencies.
# - We don’t need python-dotenv if we aren’t running network tests (and on some
#   older releases, it is too old.)
sed -r \
    -e 's/^\-e/# &/' \
    -e 's/^(pytest-benchmark|perf_baseline)\b/# &/' \
    requirements.txt | tee requirements-filtered.txt

%build
%pyproject_build

%install
%pyproject_install

%check

%if_without net_check
# All of the following require network access:
k="${k-}${k+ and }not TestClientApplicationAcquireTokenSilentErrorBehaviors"
k="${k-}${k+ and }not TestClientApplicationAcquireTokenSilentFociBehaviors"
k="${k-}${k+ and }not TestClientApplicationForAuthorityMigration"
k="${k-}${k+ and }not TestTelemetryMaintainingOfflineState"
k="${k-}${k+ and }not TestClientApplicationWillGroupAccounts"
k="${k-}${k+ and }not TestClientCredentialGrant"
k="${k-}${k+ and }not TestScopeDecoration"
k="${k-}${k+ and }not (TestAuthority and test_unknown_host_wont_pass_instance_discovery)"
k="${k-}${k+ and }not (TestAuthority and test_wellknown_host_and_tenant)"
k="${k-}${k+ and }not (TestAuthority and test_wellknown_host_and_tenant_using_new_authority_builder)"
k="${k-}${k+ and }not TestAuthorityInternalHelperUserRealmDiscovery"
k="${k-}${k+ and }not TestCcsRoutingInfoTestCase"
k="${k-}${k+ and }not TestApplicationForRefreshInBehaviors"
k="${k-}${k+ and }not TestTelemetryOnClientApplication"
k="${k-}${k+ and }not TestTelemetryOnPublicClientApplication"
k="${k-}${k+ and }not TestTelemetryOnConfidentialClientApplication"
# Without network access, these even error during test collection!
ignore="${ignore-} --ignore=tests/test_cryptography.py"
ignore="${ignore-} --ignore=tests/test_e2e.py"
%endif

# We don’t need or want to run benchmarks.
ignore="${ignore-} --ignore=tests/test_benchmark.py"

%pyproject_run_pytest --disable-warnings tests ${ignore-} -k "${k-}" -v


%files
%doc README.md
%python3_sitelibdir/msal/
%python3_sitelibdir/msal-%version.dist-info

%changelog
* Thu Oct 12 2023 Danilkin Danila <danild@altlinux.org> 1.25.0-alt1
- Initial build for Sisyphus
