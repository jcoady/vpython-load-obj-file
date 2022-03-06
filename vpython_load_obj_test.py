from vpython import *
from pywavefront import Wavefront

box1 = Wavefront('box-V3F.obj')
box2 = Wavefront('box-C3F_V3F.obj')
box3 = Wavefront('box-N3F_V3F.obj')
box4 = Wavefront('box-T2F_V3F.obj')
box5 = Wavefront('box-T2F_C3F_V3F.obj')
box6 = Wavefront('box-T2F_N3F_V3F.obj')

scene = canvas()
scene.ambient=color.gray(0.5)

def obj_to_triangles(obj): # specify object
    tris = [] # list of triangles to compound
    ret = [] # will return a list obj compounds if necessary
    # Iterate vertex data collected in each material
    for name, mesh in obj.meshes.items():
        vertices = 0
        curtexture = None
        curcol = vec(1,1,1)
        curopacity = 1.0
        # Contains the vertex format (string) such as "T2F_N3F_V3F"
        # T2F, C3F, N3F and V3F may appear in this string
        for material in mesh.materials:
            # Contains the vertex format (string) such as "T2F_N3F_V3F"
            # T2F, C3F, N3F and V3F may appear in this string
            curopacity = material.transparency
            #print(vars(material))
            #print(vars(material.texture))
            if material.vertex_format == 'V3F':
                vertex_size = 3
            elif material.vertex_format == 'C3F_V3F':
                vertex_size = 6
            elif material.vertex_format == 'N3F_V3F':
                vertex_size = 6
            elif material.vertex_format == 'T2F_V3F':
                vertex_size = 5
                curtexture = str(material.texture._path)
                #curtexture = str(material.texture._search_path) + '/' + material.texture._name
            elif material.vertex_format == 'T2F_C3F_V3F':
                vertex_size = 8
                curtexture = str(material.texture._path)
            elif material.vertex_format == 'T2F_N3F_V3F':
                vertex_size = 8
                curtexture = str(material.texture._path)
            verts = []
            for i in range(len(material.vertices)//vertex_size):
                if material.vertex_format == 'V3F':
                    curpos = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],material.vertices[i*vertex_size+2])
                    verts.append( vertex(pos=curpos) )
                elif material.vertex_format == 'C3F_V3F':
                    curcol = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],material.vertices[i*vertex_size+2])
                    curpos = vec(material.vertices[i*vertex_size+3],material.vertices[i*vertex_size+4],material.vertices[i*vertex_size+5])
                    verts.append( vertex(pos=curpos,color=curcol) )
                elif material.vertex_format == 'N3F_V3F':
                    normal = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],material.vertices[i*vertex_size+2])
                    curpos = vec(material.vertices[i*vertex_size+3],material.vertices[i*vertex_size+4],material.vertices[i*vertex_size+5])
                    verts.append( vertex(pos=curpos,normal=normal) )
                elif material.vertex_format == 'T2F_V3F':
                    curtexpos = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],0)
                    curpos = vec(material.vertices[i*vertex_size+2],material.vertices[i*vertex_size+3],material.vertices[i*vertex_size+4])
                    verts.append( vertex(pos=curpos,texpos=curtexpos) )
                elif material.vertex_format == 'T2F_C3F_V3F':
                    curtexpos = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],0)
                    curcol = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],material.vertices[i*vertex_size+2])
                    curpos = vec(material.vertices[i*vertex_size+5],material.vertices[i*vertex_size+6],material.vertices[i*vertex_size+7])
                    verts.append( vertex(pos=curpos, texpos=curtexpos, color=curcol) )
                elif material.vertex_format == 'T2F_N3F_V3F':
                    curtexpos = vec(material.vertices[i*vertex_size],material.vertices[i*vertex_size+1],0)
                    normal = vec(material.vertices[i*vertex_size+2],material.vertices[i*vertex_size+3],material.vertices[i*vertex_size+4])
                    curpos = vec(material.vertices[i*vertex_size+5],material.vertices[i*vertex_size+6],material.vertices[i*vertex_size+7])
                    verts.append( vertex(pos=curpos,normal=normal,texpos=curtexpos) )
                    
                verts[-1].opacity = curopacity
                if len(verts) == 3:
                    vertices += 3
                    tris.append(triangle(vs=verts))
                    verts=[]

                if vertices > 64000:
                    print(vertices)
                    if curtexture is not None:
                        ret.append(compound(tris,texture=curtexture))
                    else:
                        ret.append(compound(tris))
                    tris = []
                    vertices = 0
                    
            if curtexture is not None:
                ret.append(compound(tris,texture=curtexture))
            else:
                ret.append(compound(tris))
            tris = []
            vertices = 0

    if len(ret) == 1: return ret[0]               
    else: return ret
                                 


boxes = []
boxes.append(obj_to_triangles(box1))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(-4,2,0)
boxes.append(obj_to_triangles(box2))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(0,2,0)
boxes.append(obj_to_triangles(box3))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(4,2,0)
boxes.append(obj_to_triangles(box4))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(-4,-2,0)
boxes.append(obj_to_triangles(box5))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(0,-2,0)
boxes.append(obj_to_triangles(box6))
boxes[-1].visible = True
boxes[-1].up = vec(1,1,1)
boxes[-1].pos = vec(4,-2,0)

while True:
  rate(60)
  for b in boxes:
    b.rotate(angle=.02, axis=vector(0,1,0))
