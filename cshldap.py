import ldap
import ldap.sasl

class CSHLDAP():

	def __init__(self, host):
		self.host = host
		try:
			self.conn = ldap.initialize(self.host)
			auth = ldap.sasl.gssapi("")
			self.conn.sasl_interactive_bind_s("",auth)
			self.conn.set_option(ldap.OPT_DEBUG_LEVEL,0)
		except ldap.LDAPError, e:
			print (e)
	
	def search(self, search_dn,search_filter):
		try:
			res = self.conn.search_s(search_dn,ldap.SCOPE_SUBTREE, search_filter)
			return res
		except ldap.LDAPError, e:
			print (e)

			return 'Error encountered.'


