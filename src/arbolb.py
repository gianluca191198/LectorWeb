

class NodoArbolB(object):

	"""Nodo base de un arbol B.
	
	Argumentos:
	orden -- La cantidad de hijos que un nodo puede tener
	tipo -- El tipo de objeto a almacenar. Note requiere la clase en si, es decir,
	el retorno de la funcion type().
	Por ejemplo, para crear un nodo que almacene enteros con capacidad para 4:
	BTreeNode(5, int) o BTreeNode(5, type(1))
	"""
	def __init__(self, orden, tipo):
		self.elementos = []
		self.padre = None
		self.hijos = []
		self.orden = orden
		self.tipo = tipo

	def insertar(self, elemento):
		if type(elemento) != self.tipo:
			raise TipoIncompatible('El elemento a insertar no es del tipo correspondiente al arbol')

		if len(self.elementos) < self.orden - 1:
			for x in range(len(self.elementos)):
				if self.elementos[x] > elemento:
					self.elementos.append(elemento)
					_desplazar_(elemento, x)
					break
				elif self.elementos[x] == elemento:
					break
			else:
				self.elementos.append(elemento)

		elif len(self.hijos) == 0:
			for x in range(len(self.elementos)):
				if self.elementos[x] > elemento:
					self._partir_(elemento, x)
					break
			else:
				self._partir_(elemento, len(self.elementos))
		else:
			pos = 0
			while pos <= self.ultima_pos:
				if self.elementos[pos] > elemento:
					self.hijos[pos].insertar(elemento)
					break
				pos += 1
			else:
				print(self.hijos[-1].elementos)
				self.hijos[-1].insertar(elemento)
			

	def _desplazar_(self, reemplazo, pos):
		if pos == len(self.elementos):
			return
		temp = self.elementos[pos]
		self.elementos[pos] = reemplazo
		self._desplazar_(temp, pos+1)

	def _partir_(self, elemento, pos):
		temp = self.elementos[int(len(self.elementos)/2):]
		self.elementos = self.elementos[:int(len(self.elementos)/2)]
		if pos > int(len(self.elementos)/2):
			temp.append(elemento)
		else:
			self.insertar(elemento)
			temp.append(self.elementos.pop(-1))

		if self.padre:
			self.padre._agregar_hijo_(temp[0])
			for item in temp:
				self.padre.insertar(item)
		else:
			self.padre = NodoArbolB(self.orden, self.tipo)
			self.padre._convertir_en_padre_(temp, self)

	def _convertir_en_padre_(self, elementos_a_distribuir, hijo):
		for x in range(self.orden-1):
			self.elementos.append(None)
		self.elementos[0] = elementos_a_distribuir[0]
		self.hijos.append(hijo)
		self.hijos[-1].padre = self
		self.hijos.append(NodoArbolB(self.orden, self.tipo))
		self.hijos[-1].padre = self
		print(self.hijos[-1].elementos)
		self.ultima_pos = 0
		for item in elementos_a_distribuir:
			self.insertar(item)

	def _agregar_hijo_(self, clave):
		try:
			self.ultima_pos += 1
			self.elementos[self.ultima_pos] = clave
			self.hijos.append(NodoArbolB(self.orden, self.tipo))
			self.hijos[-1].padre = self
		except IndexError:
			self._partir_(clave, self.orden-1)

	def obtener_raiz(self):
		if self.padre:
			return self.padre.obtener_raiz()
		else:
			return self

class TipoIncompatible(Exception):
	pass