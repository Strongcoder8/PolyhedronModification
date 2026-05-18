from math import pi, sqrt
from functools import reduce
from operator import add
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Segment:
    """ Одномерный отрезок """
    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin

    def is_degenerate(self):
        return self.beg >= self.fin

    def intersect(self, other):
        if other.beg > self.beg:
            self.beg = other.beg
        if other.fin < self.fin:
            self.fin = other.fin
        return self

    def subtraction(self, other):
        return [Segment(
            self.beg, self.fin if self.fin < other.beg else other.beg),
            Segment(self.beg if self.beg > other.fin else other.fin, self.fin)]


class Edge:
    """ Ребро полиэдра """
    SBEG, SFIN = 0.0, 1.0

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin
        self.gaps = [Segment(Edge.SBEG, Edge.SFIN)]

    def shadow(self, facet):
        if facet.is_vertical():
            return
        shade = Segment(Edge.SBEG, Edge.SFIN)
        for u, v in zip(facet.vertexes, facet.v_normals()):
            shade.intersect(self.intersect_edge_with_normal(u, v))
            if shade.is_degenerate():
                return

        shade.intersect(
            self.intersect_edge_with_normal(
                facet.vertexes[0], facet.h_normal()))
        if shade.is_degenerate():
            return
        gaps = [s.subtraction(shade) for s in self.gaps]
        self.gaps = [
            s for s in reduce(add, gaps, []) if not s.is_degenerate()]

    def r3(self, t):
        return self.beg * (Edge.SFIN - t) + self.fin * t

    def intersect_edge_with_normal(self, a, n):
        f0, f1 = n.dot(self.beg - a), n.dot(self.fin - a)
        if f0 >= 0.0 and f1 >= 0.0:
            return Segment(Edge.SFIN, Edge.SBEG)
        if f0 < 0.0 and f1 < 0.0:
            return Segment(Edge.SBEG, Edge.SFIN)
        x = - f0 / (f1 - f0)
        return Segment(Edge.SBEG, x) if f0 < 0.0 else Segment(x, Edge.SFIN)

    def reset_gaps(self):
        self.gaps = [Segment(Edge.SBEG, Edge.SFIN)]


class Facet:
    """ Грань полиэдра """
    def __init__(self, vertexes, edges=None):
        self.vertexes = vertexes
        self.edges = edges if edges is not None else []

    def is_vertical(self):
        return self.h_normal().dot(Polyedr.V) == 0.0

    def h_normal(self):
        n = (self.vertexes[1] - self.vertexes[0]).cross(
             self.vertexes[2] - self.vertexes[0])
        return n * (-1.0) if n.dot(Polyedr.V) < 0.0 else n

    def v_normals(self):
        return [self._vert(x) for x in range(len(self.vertexes))]

    def _vert(self, k):
        n = (self.vertexes[k] - self.vertexes[k - 1]).cross(Polyedr.V)
        return n * \
            (-1.0) if n.dot(self.vertexes[k - 1] - self.center()) < 0.0 else n

    def center(self):
        return sum(self.vertexes, R3(0.0, 0.0, 0.0)) * \
            (1.0 / len(self.vertexes))


class Polyedr:
    """ Полиэдр """
    V = R3(0.0, 0.0, 1.0)

    def __init__(self, file):
        self.vertexes, self.edges, self.facets = [], [], []

        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    buf = line.split()
                    c = float(buf.pop(0))
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    x, y, z = (float(x) for x in line.split())
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    buf = line.split()
                    size = int(buf.pop(0))
                    vertexes = list(self.vertexes[int(n) - 1] for n in buf)
                    facet_edges = []
                    for n in range(size):
                        e = Edge(vertexes[n - 1], vertexes[n])
                        self.edges.append(e)
                        facet_edges.append(e)
                    self.facets.append(Facet(vertexes, facet_edges))

    def reset_all_gaps(self):
        for e in self.edges:
            e.reset_gaps()

    def shadow(self):
        """ Нахождение «просветов» на всех рёбрах """
        for e in self.edges:
            for f in self.facets:
                e.shadow(f)
        return self

    # -------------------- Характеристика --------------------
    def _is_fully_visible_edge(self, edge):
        return (len(edge.gaps) == 1 and
                edge.gaps[0].beg == 0.0 and
                edge.gaps[0].fin == 1.0)

    def _is_fully_invisible_edge(self, edge):
        return len(edge.gaps) == 0

    def _perimeter(self, facet):
        total = 0.0
        for e in facet.edges:
            dx = e.fin.x - e.beg.x
            dy = e.fin.y - e.beg.y
            dz = e.fin.z - e.beg.z
            total += sqrt(dx * dx + dy * dy + dz * dz)
        return total

    def get_partial_visible_perimeter_outside_square(self):
        self.reset_all_gaps()
        self.shadow()
        total = 0.0
        for facet in self.facets:
            fully_vis = True
            fully_invis = True
            for edge in facet.edges:
                if self._is_fully_visible_edge(edge):
                    fully_invis = False
                elif self._is_fully_invisible_edge(edge):
                    fully_vis = False
                else:
                    fully_vis = False
                    fully_invis = False
                    break
            if fully_vis or fully_invis:
                continue
            c = facet.center()
            if abs(c.x) > 0.5 or abs(c.y) > 0.5:
                total += self._perimeter(facet)
        return total

    # -------------------- Отрисовка --------------------
    def draw(self, tk):
        tk.clean()
        self.shadow()
        for e in self.edges:
            for s in e.gaps:
                tk.draw_line(e.r3(s.beg), e.r3(s.fin))
